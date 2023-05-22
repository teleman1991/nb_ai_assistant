import os.path

import pdfplumber as pdfplumber
import PyPDF4 as PyPDF4

from app_types import PageMetadata, PDFDocumentMetadata, ListPagesData
from utils import merge_hyphenated_words, fix_newlines, remove_multiple_newlines, clean_text


def extract_pages_from_pdf(file_path: str) -> ListPagesData:
    """
    Extracts the text from each page of the PDF.
    :param file_path: - The path of the PDF file.
    :return: - A list of tuples, containing the page number and the extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with pdfplumber.open(file_path) as pdf:
        pages = []
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text.strip():  # Check if extracted text exists.
                pages.append((page_num + 1, text))

    return pages


# TODO: Check if it could be done in data of the next structure:
#  Document:
#   title
#   author
#   creationDate
#   pages = [(page_number, page_content)]
def extract_metadata_from_pdf(file_path: str) -> PageMetadata:
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF4.PdfFileReader(pdf_file)
        metadata = reader.getDocumentInfo()

        return {
            'title': metadata.get('/Title').strip(),
            'author': metadata.get('/Author').strip(),
            'creation_date': metadata.get('/CreationDate').strip(),
        }


def parse_pdf(file_path: str) -> PDFDocumentMetadata:
    """
    Extracts the title and text from each page of the PDF.

    :param file_path: - The path of the PDF file.
    :return: The tuple containing the title and list of tuples with page numbers
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    metadata: PageMetadata = extract_metadata_from_pdf(file_path)
    pages: ListPagesData = extract_pages_from_pdf(file_path)

    return pages, metadata


if __name__ == "__main__":
    file_path = './Nifty Bridge Terms of Service.pdf'
    raw_pages, metadata = parse_pdf(file_path)

    # TODO: Write unit tests for each of them.
    cleaning_functions_queue = [
        merge_hyphenated_words,
        fix_newlines,
        remove_multiple_newlines,
    ]

    cleaned_text_pdf = clean_text(
        raw_pages,
        cleaning_functions_queue
    )
    text_chunks = text_to_chunks(cleaned_text_pdf, metadata)