from typing import List
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class PageData:
    num: int
    text: str


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


class OKResponse(BaseModel):
    message: str


class BadRequestResponse(BaseModel):
    detail: str


class UnauthorizedResponse(BaseModel):
    detail: str
