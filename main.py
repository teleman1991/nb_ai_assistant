from config import API_KEY
from fastapi import FastAPI, Depends, Request, Header, HTTPException
from http import HTTPStatus

app = FastAPI()


from langchain.text_splitter import RecursiveCharacterTextSplitter


def validate_api_key(API_KEY_Token: str = Header(None, convert_underscores=True)):  # noqa
    if API_KEY_Token == API_KEY:
        return True
    return False


async def check_api_key(X_API_KEY_Token: str = Header(None, convert_underscores=True)):  # noqa
    is_valid = validate_api_key(X_API_KEY_Token)
    if not is_valid:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    return None


@app.post("/api/send", dependencies=[Depends(check_api_key)])
async def send(request: Request):
    data = await request.json()
    if data.get('message', None) is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    # Count TOKENS. Check if it does not exceed MAX_TOKENS
    # Load prompts.
    return {"message": "Hello I am NiftyBridge AI assistant. How could I help you?"}


"""
curl -d '{"message": "Hello"}' \
-X POST "http://localhost:3000/api/send" \
-H "X-API-KEY-Token: {api_key_from_env}" \
-H "Content-Type: application/json"
—------------
{ "message": "Hello I am NiftyBridge AI assistant. How could I help you?" }
"""