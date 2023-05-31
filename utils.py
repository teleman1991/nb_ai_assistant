from typing import Callable

import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

from app_types import List, PageData, PDFDocument, MessageType
import re

from config import VECTOR_STORE_COLLECTION_NAME, VECTOR_STORE_PATH, MAX_RESPONSE_TOKENS, GPT_3_5_TURBO_TOKEN_LIMIT


def merge_hyphenated_words(text: str) -> str:
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text: str) -> str:
    return re.sub(r"(?<!\n)\n(?!\n)", r" ", text)


def remove_multiple_newlines(text: str) -> str:
    return re.sub(r"\n{2,}", r"\n", text)


def clean_text(pages: List[PageData], cleaning_functions: List[Callable[[str], str]]) -> List[PageData]:
    cleaned_pages = []
    for page_data in pages:
        text = page_data.text
        for cleaning_function in cleaning_functions:
            text = cleaning_function(text)

        cleaned_pages.append(PageData(num=page_data.num, text=text))

    return cleaned_pages


def text_to_chunks(pdf_document: PDFDocument) -> List[Document]:
    """
    Converts list of strings into list of Documents with metadata.
    :param pdf_document:
    :return:
    """

    doc_chunks = []

    for page in pdf_document.pages:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=200
        )
        split_chunks = text_splitter.split_text(page.text)
        for i, each_chunk in enumerate(split_chunks):
            doc_chunk = Document(
                page_content=each_chunk,
                metadata={
                    "page_number":page.num,
                    "chunk": i,
                    "source": f"p{page.num}-{i}",
                    **pdf_document.metadata,
                }
            )

            doc_chunks.append(doc_chunk)

    return doc_chunks


def make_chain():
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, max_tokens=MAX_RESPONSE_TOKENS)
    embedding = OpenAIEmbeddings()
    vector_store = Chroma(
        collection_name=VECTOR_STORE_COLLECTION_NAME,
        embedding_function=embedding,
        persist_directory=VECTOR_STORE_PATH
    )

    return ConversationalRetrievalChain.from_llm(
        model,
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )


def generate_ai_response(chain, chat_history: list, question: str) -> str:
    # Use the template and the question to generate a response using the AI model
    response = chain(
        {
            "question": question,
            'chat_history': chat_history
        }
    )
    answer = response["answer"]

    return answer


def limit_tokens_for_request(question: str, chat_history: List[MessageType]) -> List[MessageType]:
    """
    :param question:        The question to the model. Is used to count tokens only. WIll stay the same.
    :param chat_history:    Collection of previous messages within the discussion.
                             In case of too many messages, older ones will be cut off, leaving newer ones.
    :return: limited history
    :raises ValueError in case, if question has too many tokens provided.
    """

    result_chat_history: List[MessageType] = []

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Counting necessary token waste.
    tokens_count = MAX_RESPONSE_TOKENS  # Expected that tokens to be wasted by the model to respond user.
    tokens_count += 2  # every reply (in the end) is primed with <im_start>assistant

    # Counting question tokens.
    tokens_count += 4  # Every message follows <im_start>[role/name]\n(content)<im_end>\n
    tokens_count += len(encoding.encode(question))

    # Counting chat history tokens.
    for message in reversed(chat_history):
        current_message_tokens = len(encoding.encode(message.content))
        current_message_tokens += 4  # Every message follows <im_start>[role/name]\n(content)<im_end>\n
        current_message_tokens += 1  # role is always required, and always 1 token

        if tokens_count + current_message_tokens < GPT_3_5_TURBO_TOKEN_LIMIT * 0.8:  # 80% of limit, for safe.
            result_chat_history.insert(0, message.copy())
            tokens_count += current_message_tokens

    if tokens_count >= GPT_3_5_TURBO_TOKEN_LIMIT * 0.9:
        raise ValueError("Too much tokens for model")

    return result_chat_history
