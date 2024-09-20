from fastapi import UploadFile
from sqlalchemy.orm import Session

import shutil
import hashlib

from . import modules, schemas

def create_ticket(ticket: schemas.TicketCreate,db: Session):
    
    db_ticket = modules.Ticket(
        contact = ticket.contact
    )

    if ticket.name:
        db_ticket.name = ticket.name

    if ticket.discription:
        db_ticket.discription=ticket.discription
    
    if ticket.problem_type in [0,1,2]:
        db_ticket.problem_type=ticket.problem_type
    
    if ticket.help_type in [0,1,2,3]:
        db_ticket.help_type=ticket.help_type
    
    if ticket.hope_time:
        db_ticket.hope_date=ticket.hope_time

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def create_file(file: UploadFile, ticket_id:int,db: Session):
    # TODO file upload to other place

    # hash
    hash_func = hashlib.sha256()
    while chunk := file.file.read(25536):
        hash_func.update(chunk)
    hash_name=hash_func.hexdigest()
    # pointer to start
    file.file.seek(0)

    # save to local
    with open(f"uploads/{hash_name}.{file.content_type.split('/')[-1]}", "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # db
    db_file=modules.Image(
        uri=f"uploads/{hash_name}.{file.content_type}",
        ticket_id=ticket_id,
        size=file.size
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file