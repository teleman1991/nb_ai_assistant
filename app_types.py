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

    @property
    def metadata(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "creation_date": self.creation_date,
        }
