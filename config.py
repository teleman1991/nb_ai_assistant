import os

API_KEY = os.environ.get("API_KEY", None)
assert API_KEY is not None, "API_KEY environment variable should be set to let API callers authorize themselves"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
assert OPENAI_API_KEY is not None, "OPENAI_API_KEY environment variable should be set to let API callers authorize " \
                                   "themselves"

VECTOR_STORE_COLLECTION_NAME = 'terms_of_service'
