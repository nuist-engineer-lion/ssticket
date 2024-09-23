from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

ProblemType=["疑问","故障","清理"]
HelpType=["软件问题","硬件问题","两者都有","其他问题"]


class Worker(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)
    contact = Column(String)
    available = Column(Boolean,default=False)
    lark_id = Column(String,nullable=True)

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    contact = Column(String)
    name = Column(String, nullable=True)

    description = Column(Text,nullable=True)
    # 0:question 1:error 2:clean
    problem_type = Column(Integer,nullable=True)
    # 0:software 1:hardware 2:both 3:other
    help_type = Column(Integer,nullable=True)

    hope_date = Column(DateTime,nullable=True)

    handled = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now)

    worker_id = Column(Integer,ForeignKey('workers.id'),nullable=True)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer,primary_key=True)
    uri = Column(String)
    size = Column(Integer)
    ticket_id = Column(Integer,ForeignKey('tickets.id'))