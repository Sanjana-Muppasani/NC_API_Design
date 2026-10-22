from pydantic import BaseModel
from datetime import datetime 

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    location: str
    address: str | None
    capacity: int
    created_at: datetime

class EventDetailResponse(BaseModel):
    event: EventResponse

class EventsResponse(BaseModel): 
    events : list