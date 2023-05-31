from typing import List, Union
from dataclasses import dataclass

from langchain.schema import HumanMessage, AIMessage
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


MessageType = Union[HumanMessage, AIMessage]


class OKResponse(BaseModel):
    message: str


class BadRequestResponse(BaseModel):
    detail: str


class UnauthorizedResponse(BaseModel):
    detail: str
