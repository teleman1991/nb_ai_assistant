from typing import List
from dataclasses import dataclass


@dataclass
class PageData:
    number: int
    content: str


@dataclass
class PDFDocument:
    title: str
    author: str
    creation_date: str
    pages: List[PageData]



