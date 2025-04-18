# app/models/search_models.py
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list[str]

class ErrorResponse(BaseModel):
    error: str