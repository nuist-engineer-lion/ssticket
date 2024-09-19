from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import modules, schemas

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    # TODO 数据校验
    db_ticket = modules.Ticket(
        qq = ticket.qq
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

def create_file(db: Session, file: UploadFile, ticket_id:int):
    # TODO file upload and get uri
    # TODO 文件格式校验
    ...