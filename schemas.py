import datetime
from typing import List
from fastapi import UploadFile
from pydantic import BaseModel

class TicketCreate(BaseModel):
    name: str | None = None
    contact: str

    discription:str | None = None
    # 0:question 1:error 2:clean
    problem_type: int | None = None
    # 0:software 1:hardware 2:both 3:other
    help_type: int | None = None

    hope_time: datetime.datetime | None = None

    files: List[UploadFile] | None = None

class WorkerCreate(BaseModel):
    name:str
    contact:str