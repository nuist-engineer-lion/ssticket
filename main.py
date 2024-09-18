from fastapi import FastAPI,Depends,File,UploadFile
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ticket")
async def upload(ticket:schemas.TicketCreate,db:Session = Depends(get_db)):
    
    return 200
