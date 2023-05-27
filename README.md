# Server AI assistant FastAPI Application

This repository contains a FastAPI application of AI assitant. It provides an API for posting question, and get reponse
based on rules, decripted with natural language, being stored in PDF document.

## Features

- Registration of user's API keys.
- PDF document parsing and embedding.
- FastAPI application.

## Installation

### Using Docker

1. Get and install Docker for your operating system: ~[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)~

2. Run the server by executing:
`docker run -p 8000:8000 -e OPENAI_API_KEY=<Your openai key> boshtannik/nb_ai_assistant`

Currently, your server does not have any API_KEYS for users to be authed with. And server does not have PDF document
being embedded.
To do this:

3. Get name or ID of running container, by run:
`docker ps -a`
4. Use CONTAINER ID to parse PDF document and make it embedded. Run:
`docker exec -e OPENAI_API_KEY=<Your openai key> <CONTAINER ID> python persist_document.py`
5. use CONTAINER ID to register new API_KEY to access the server:
`docker exec <CONTAINER ID> python user_api_key_registrator.py --register`
Now you will see new registered API_KEY, that user may use to access the API endpoint.

6. - Done. User now can access server, by providing API_KEY

### Manual Run

1. Make sure you have Python 3.11 installed.
2. Optionally, create and activate a virtual environment.
3. Upgrade pip: `pip install --upgrade pip`
4. Install required dependencies: `pip install -r requirements.txt`

### Parsing and Embedding PDF

1. Run: `OPENAI_API_KEY=<Your openai key> python persist_document.py`

### Registering Users

1. Register a new user: `python user_api_key_registrator.py --register`
2. List registered API keys: `python user_api_key_registrator.py --list`

### Running the Server

1. Start the server: `OPENAI_API_KEY=<Your OPENAI key here> uvicorn main:app --host 0.0.0.0 --port 8000`

Now, users can access the server using their API key.

### Usage
Usage be like:
`curl -d '{"message": "Hello"}' -X POST "http://localhost:8000/api/send" -H "X-API-KEY-Token: {API_KEY}" -H "Content-Type: application/json"`
