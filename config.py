import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

VECTOR_STORE_COLLECTION_NAME = 'terms_of_service'
VECTOR_STORE_PATH = 'src/data/chroma'
if not os.path.exists(VECTOR_STORE_PATH):
    os.makedirs(VECTOR_STORE_PATH)


USERS_API_KEYS_DB_FILE = './users.sqlite3'
