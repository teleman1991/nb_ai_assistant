import sqlite3

from config import USERS_API_KEYS_DB_FILE, OPENAI_API_KEY
from fastapi import FastAPI, Depends, Request, Header, HTTPException
from http import HTTPStatus
from langchain.schema import AIMessage, HumanMessage
from utils import make_chain

assert OPENAI_API_KEY is not None, "OPENAI_API_KEY environment variable should be set to let API callers authorize " \
                                   "themselves"

from db_services import get_user_id_by_api_key, load_chat_history, re_initialize_db, save_chat_history

app = FastAPI()


async def check_api_key(X_API_KEY_Token: str = Header(None, convert_underscores=True)):  # noqa.
    with sqlite3.Connection(USERS_API_KEYS_DB_FILE) as db_connection:
        re_initialize_db(db_connection)
        user_id = get_user_id_by_api_key(db_connection, X_API_KEY_Token)

    if user_id is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    return user_id


@app.post("/api/send", dependencies=[Depends(check_api_key)])
async def send(request: Request, user_id: int = Depends(check_api_key)):
    data = await request.json()
    request_question = data.get('message', None)

    if request_question is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    with sqlite3.Connection(USERS_API_KEYS_DB_FILE) as db_connection:
        chain = make_chain()
        chat_history = load_chat_history(db_connection, user_id)

        response = chain({"question": request_question, "chat_history": chat_history})

        answer = response["answer"]
        # source = response["source_documents"] - Might be used in order to point exact page and line

        new_messages = [
            HumanMessage(content=request_question),
            AIMessage(content=answer)
        ]

        save_chat_history(db_connection=db_connection, messages=new_messages, user_id=user_id)

    # Return answer
    return {"message": answer}


"""
curl -d '{"message": "Hello"}' \
-X POST "http://localhost:3000/api/send" \
-H "X-API-KEY-Token: {api_key_from_env}" \
-H "Content-Type: application/json"
—------------
{ "message": "Hello I am NiftyBridge AI assistant. How could I help you?" }
"""