import datetime

from pydantic import BaseModel


class Event(BaseModel):
    artists: list[str]
    date: datetime.date
