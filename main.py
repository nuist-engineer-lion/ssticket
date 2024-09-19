from fastapi import FastAPI,Depends,File,UploadFile,Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import modules, schemas, crud
from .database import SessionLocal, engine

from typing import Annotated
import os

modules.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static/", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ticket",status_code=201)
async def upload_ticket_form(
    ticket:Annotated[schemas.TicketCreate,File()],
    db:Session = Depends(get_db),
    ):
    
    db_ticket = crud.create_ticket(db,ticket)
    
    # TODO 添加文件处理

    # TODO 重定向到成员页
    return db_ticket

# TODO 空闲成员推荐