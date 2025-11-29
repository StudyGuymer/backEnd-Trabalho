# app/schemas.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime

class NewsBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, example="Notícia importante")
    summary: Optional[str] = Field(None, max_length=500, example="Resumo breve da notícia")
    content: str = Field(..., min_length=10, example="Conteúdo completo da notícia")
    author: Optional[str] = Field(None, max_length=100, example="Nome do autor")
    image_url: Optional[HttpUrl] = None

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, min_length=10)
    author: Optional[str] = Field(None, max_length=100)
    image_url: Optional[HttpUrl] = None

class NewsOut(NewsBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
