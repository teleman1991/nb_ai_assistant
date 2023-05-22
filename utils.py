from typing import Callable

from app_types import List, PageData
import re


def merge_hyphenated_words(text: str) -> str:
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text: str) -> str:
    return re.sub(r"(?<!\n)\n(?!\n)", r" ", text)


def remove_multiple_newlines(text: str) -> str:
    return re.sub(r"\n{2,}", r"\n", text)


def clean_text(pages: List[PageData], cleaning_functions: List[Callable[[str], str]]) -> List[PageData]:
    cleaned_pages = []
    for page_data in pages:
        text = page_data.content
        for cleaning_function in cleaning_functions:
            text = cleaning_function(text)
        cleaned_pages.append(
            PageData(number=page_data.number, content=text)
        )
    return cleaned_pages
