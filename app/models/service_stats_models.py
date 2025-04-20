from pydantic import BaseModel

class ServiceStatsResponse(BaseModel):
    status: str
    dbSize: str
    documentCount: int
    lastUpdated: str