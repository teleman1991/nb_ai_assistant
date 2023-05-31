import sqlite3

from app_types import OKResponse, BadRequestResponse, UnauthorizedResponse
from config import USERS_API_KEYS_DB_FILE, OPENAI_API_KEY
from fastapi import FastAPI, Depends, Request, Header, HTTPException, status
from http import HTTPStatus
from langchain.schema import AIMessage, HumanMessage
from utils import make_chain, generate_ai_response, limit_tokens_for_request
from langchain import PromptTemplate
from db_services import get_user_id_by_api_key, load_chat_history, re_initialize_db, save_to_chat_history


assert OPENAI_API_KEY is not None, "OPENAI_API_KEY environment variable should be set to let API callers authorize " \
                                   "themselves"

app = FastAPI()


async def check_api_key(X_API_KEY_Token: str = Header(None, convert_underscores=True)):  # noqa.
    with sqlite3.Connection(USERS_API_KEYS_DB_FILE) as db_connection:
        re_initialize_db(db_connection)
        user_id = get_user_id_by_api_key(db_connection, X_API_KEY_Token)

    if user_id is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    return user_id


@app.post(
    "/api/send",
    dependencies=[Depends(check_api_key)],
    summary="Send a message to the AI assistant",
    description="Send a message to the AI assistant and receive a response. The AI assistant will generate a"
                " response based on the message and the chat history.",
    tags=['/api/send'],
    responses={
        status.HTTP_200_OK: {
            "description": "OK: The AI assistant successfully processed the message and generated a response.",
            "model": OKResponse,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request: The provided message is invalid or not found.",
            "model": BadRequestResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized: The provided API key is invalid or not found.",
            "model": UnauthorizedResponse,
        },
    },
)
async def send(request: Request, user_id: int = Depends(check_api_key)):
    data = await request.json()
    request_question = data.get('message', None)

    if request_question is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    with sqlite3.Connection(USERS_API_KEYS_DB_FILE) as db_connection:
        chat_history = load_chat_history(db_connection, user_id)

        # Integrate the template into the send function
        prompt_template = PromptTemplate(
            input_variables=['query'],
            template="""
            Greet user with calling yourself "NiftyBridge AI assistant".
            Give answers only from the answer from vectorstore documents.
            You should not answer questions, that are not related to "Nifty Bridge" program, described in the document.
            In the case, that the answer is not provided within the context, say: "i don't know please contact with support by email support@nifty-bridge.com".
            
            Question: {query}
            Answer:"""  # noqa
        )

        chain = make_chain()

        question = prompt_template.format(query=request_question)
        try:
            limited_chat_history = limit_tokens_for_request(question=question,
                                                            chat_history=chat_history)
        except ValueError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="The question is too long. Server not process this.")

        # Generate the response using the template and the AI model
        ai_response = generate_ai_response(
            chain=chain,
            question=question,
            chat_history=limited_chat_history,
        )

        new_messages = [
            HumanMessage(content=request_question),
            AIMessage(content=ai_response),
        ]

        save_to_chat_history(db_connection=db_connection, messages=new_messages, user_id=user_id)

    # Return answer
    return {"message": ai_response}
