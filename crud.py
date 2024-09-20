from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select

import shutil
import hashlib

from . import modules, schemas

import os

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

def create_worker(worker: schemas.WorkerCreate,db: Session):
    db_worker = modules.Worker(
        name=worker.name,
        contact=worker.contact
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def research_ticket_by_time(time:datetime,handled:int|None,db: Session):
    if handled:
        tickets = db.execute(select(modules.Ticket).where(modules.Ticket.create_time >= time).where(modules.Ticket.handled==handled)).scalars()
    else:
        tickets = db.execute(select(modules.Ticket).where(modules.Ticket.create_time >= time)).scalars()
    return tickets


def research_workers(avaliable:int|None,db: Session):
    if avaliable:
        workers = db.execute(select(modules.Worker).where(modules.Worker.available==avaliable)).scalars()
    else:
        workers = db.execute(select(modules.Worker)).scalars()
    return workers

def research_worker(name:str,db:Session):
    worker = db.execute(select(modules.Worker).where(modules.Worker.name==name)).scalar()
    return worker

def research_file(ticket_id:int,db:Session):
    files = db.execute(select(modules.Image).where(modules.Image.ticket_id==ticket_id)).scalars()
    return files

def update_ticket(db_ticket:modules.Ticket,discription:str|None,worker_id:int|None,handled:int|None,db:Session):
    if discription:
        db_ticket.discription = db_ticket.discription + '\n' +discription
    if worker_id:
        db_ticket.worker_id = worker_id
    if handled:
        db_ticket.handled = handled
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_worker(db_worker:modules.Worker,available:bool|None,contact:str|None,db:Session):
    if available:
        db_worker.available = available
    if contact:
        db_worker.contact = contact
    db.commit()
    db.refresh(db_worker)
    return db_worker

def delete_ticket(db_ticket:modules.Ticket,db:Session):
    files = research_file(ticket_id=db_ticket.id,db=db)
    for file in files:
        delete_file(file,db)
    db.delete(db_ticket)
    db.commit()
    

def delete_worker(db_worker:modules.Worker,db:Session):
    db.delete(db_worker)

def delete_file(db_file:modules.Image,db:Session):
    os.remove(db_file.uri)
    db.delete(db_file)
