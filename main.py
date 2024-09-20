from fastapi import FastAPI,Depends,File, HTTPException,UploadFile,Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import modules, schemas, crud
from .database import SessionLocal, engine

from typing import Annotated
import os

modules.Base.metadata.create_all(bind=engine)

class Settings(BaseSettings):
    app_name: str = "Ssticket"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
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
    
    db_ticket = crud.create_ticket(ticket,db)

    # file handler
    for file in ticket.files:
        try:
            # check
            if file.size == 0:
                break
            if file.content_type.split('/')[0] != "image":
                raise HTTPException(status_code=400,detail=file.content_type)
            # create
            crud.create_file(file,db_ticket.id,db)
        finally:
            file.file.close()
    
    # TODO 重定向到成员页
    return db_ticket

# TODO 空闲成员推荐
@app.get('/workers',status_code=200)
async def get_workers(db:Session=Depends(get_db)):
    return