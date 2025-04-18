from pydantic import BaseModel

class DataLoaderRequest(BaseModel):
    text: str

class DataLoaderResponse(BaseModel):
    message: str