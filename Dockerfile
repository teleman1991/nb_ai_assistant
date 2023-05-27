FROM python:3.11
RUN git clone https://github.com/boshtannik/nb_ai_assistant.git app/
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN echo 'Parsing pdf, split it into chunks, embed it, cache it.'
RUN python persist_document.py
RUN echo 'Embedding text chunks done'
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
