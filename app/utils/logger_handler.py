from fastapi import APIRouter, FastAPI, HTTPException, Request, logger

from models.login_log_dto import LoginLogModel
from models.work_log_dto import WorkLogModel
from db.context import login_log_collection
from db.context import work_log_collection
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

logger = logging.getLogger("uvicorn.error")

async def login_log_callback(log_in_out : str,user_email : str,success_YN : str, client_ip: str, user_agent:str):
    log_dic = {
        "log_in_out" : log_in_out,
        "user_email" : user_email,
        "user_agent" : user_agent,
        "success_YN" : success_YN,
        "client_ip" : client_ip,
    }
    log_document = dict(LoginLogModel(**log_dic))
    login_log_collection.insert_one(log_document)

async def work_log_callback(path : str, method : str, client_ip : str, user_agent : str, userId : str):
    
    log_dic = {
        "path" : path,
        "method" : method,
        "user_agent" : user_agent,
        "client_ip" : client_ip,
        "user_id" : userId,
        "exception_result" :None
    }
    log_document = dict(WorkLogModel(**log_dic))
    work_log_collection.insert_one(log_document)

async def exception_log_callback(request: Request, exc: HTTPException):
    logger.error(f"Exception details: {exc}")

    method = request.method
    path = request.url.path
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "Unknown")
    try:
        body = await request.json()
        user_id = body.get('user_id', 'ANONYMOUS')
    except Exception as e:
        user_id = 'ANONYMOUS' 

    log_dic = {
        "path" : path,
        "method" : method,
        "user_agent" : user_agent,
        "client_ip" : client_ip,
        "user_id" : user_id,
        "exception_result" : str(exc)
    }
    log_document = dict(WorkLogModel(**log_dic))
    work_log_collection.insert_one(log_document)
