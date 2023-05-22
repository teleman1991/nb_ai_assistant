import os.path

import pdfplumber as pdfplumber
import PyPDF4 as PyPDF4
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from app_types import PageData, PDFDocument
from utils import merge_hyphenated_words, fix_newlines, remove_multiple_newlines, clean_text, text_to_chunks


def fill_pages_from_pdf(file_path: str, pdf_document: PDFDocument):
    """
    Extracts the text from each page of the PDF.
    :param file_path: - The path of the PDF file.
    :param pdf_document: - Python instance of document to fill.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with pdfplumber.open(file_path) as pdf:
        pdf_document.pages = []
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text.strip():  # Check if extracted text exists.
                pdf_document.pages.append(PageData(number=page_num, content=text))


# TODO: Check if it could be done in data of the next structure:
#  Document:
#   title
#   author
#   creationDate
#   pages = [(page_number, page_content)]
def fill_metadata_from_pdf(file_path: str, pdf_document: PDFDocument):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF4.PdfFileReader(pdf_file)
        metadata = reader.getDocumentInfo()

        pdf_document.title = metadata.get('/Title').strip()
        pdf_document.author = metadata.get('/Author').strip()
        pdf_document.creation_date = metadata.get('/CreationDate').strip()


def parse_pdf(file_path: str) -> PDFDocument:
    """
    Extracts the title and text from each page of the PDF.

    :param file_path: - The path of the PDF file.
    :return: The tuple containing the title and list of tuples with page numbers
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    pdf_document = PDFDocument('', '', '', [])
    fill_metadata_from_pdf(file_path, pdf_document)
    fill_pages_from_pdf(file_path, pdf_document)

    return pdf_document


if __name__ == "__main__":
    file_path = './Nifty Bridge Terms of Service.pdf'
    raw_pages, metadata = parse_pdf(file_path)

    cleaning_functions_queue = [
        merge_hyphenated_words,
        fix_newlines,
        remove_multiple_newlines,
    ]

    cleaned_text_pdf = clean_text(
        raw_pages,
        cleaning_functions_queue
    )
    document_chunks = text_to_chunks(cleaned_text_pdf, metadata)

    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(
        document_chunks,
        embeddings,
    )