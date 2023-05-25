from typing import Callable

from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

from app_types import List, PageData, PDFDocument
import re

from config import VECTOR_STORE_COLLECTION_NAME, VECTOR_STORE_PATH


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
        cleaned_pages.append(
            PageData(num=page_data.num, text=text)
        )
    return cleaned_pages


def text_to_chunks(pdf_document: PDFDocument) -> List[Document]:
    """
    Converts list of strings into list of Documents with metadata.
    :param pdf_document:
    :return:
    """

    doc_chunks = []

    for page in pdf_document.pages:
        page_num = page.num
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
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
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    embedding = OpenAIEmbeddings()
    vector_store = Chroma(
        collection_name=VECTOR_STORE_COLLECTION_NAME,
        embedding_function=embedding,
        persist_directory=VECTOR_STORE_PATH
    )

    return ConversationalRetrievalChain.from_llm(
        model,
        max_tokens_limit=4000,
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )


def generate_ai_response(chain, chat_history: list, template: str, question: str) -> str:
    # Use the template and the question to generate a response using the AI model
    response = chain({"question": question, "template": template, 'chat_history': chat_history})
    answer = response["answer"]

    return answer
