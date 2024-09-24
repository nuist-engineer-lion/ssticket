import datetime
from fastapi import FastAPI,Depends,File, HTTPException,UploadFile,Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import modules, schemas, crud
from .database import SessionLocal, engine
from .config import Settings

from typing import Annotated
import json

import lark_oapi as lark

modules.Base.metadata.create_all(bind=engine)

settings = Settings()

lark_client = lark.Client.builder().app_id(settings.lark_id).app_secret(settings.lark_secret).build()

app = FastAPI()

# TODO a better static pagge
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
    if ticket.files:
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
    # feishu card link to chart
    # feishu bot notice
    card_json= json.dumps({"data":{
        "template_id":settings.lark_card,
        "template_version_name":settings.lark_card_v,
        "template_variable":{
            "time": datetime.datetime.strftime(db_ticket.create_time,"%Y/%m/%d %H:%M:%S"),
            "hope_date":  datetime.datetime.strftime(db_ticket.hope_date,"%Y/%m/%d %H:%M:%S"),
            "name":db_ticket.name,
            "contact":db_ticket.contact,
            "help_type":modules.HelpType[db_ticket.help_type],
            "problem_type":modules.ProblemType[db_ticket.problem_type],
            "description":db_ticket.description
        }
    },"type":"template"},ensure_ascii=False)
    request: lark.api.im.v1.CreateMessageRequest = lark.api.im.v1.CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(lark.api.im.v1.CreateMessageRequestBody.builder()
            .receive_id(settings.lark_chat)
            .msg_type("interactive")
            .content(card_json)
            .build()) \
        .build()

    # 发起请求
    response = lark_client.im.v1.message.create(request)
    if not response.success():
        lark.logger.error(
        f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

    # TODO 重定向到成员页
    return db_ticket

# TODO 空闲成员推荐
@app.get('/workers',status_code=200)
async def get_workers(db:Session=Depends(get_db)):
    # TODO need jinjia template
    db_workers = crud.research_workers(1,db) 
    return db_workers
