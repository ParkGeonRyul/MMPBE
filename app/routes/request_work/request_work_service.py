import json
import pymongo

from db.context import work_request_collection, auth_collection, user_collection
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from db.context import Database
from routes.auth import auth_service
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner
from models.work_request_dto import WorkRequestModel, UpdateWorkRequestModel
from constants import COOKIES_KEY_NAME
from utils.objectId_convert import objectId_convert
from routes._modules import list_module
from routes._modules.list_module import NotNull


async def get_request_list(request: Request, is_temprary: bool) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    projection = {"_id": 1, "user_id": 1, "request_title": 1, "customer_nm": 1, "request_date": 1, 'created_at': 1, 'updated_at': 1}
    if is_temprary:
        content = await list_module.get_collection_list(
            str(token_data['userId']),
            work_request_collection,
            None,
            int(request.query_params.get("page")),
            projection)
    else:
        content = await list_module.get_collection_list(
            str(token_data['userId']),
            work_request_collection,
            NotNull.not_null,
            int(request.query_params.get("page")),
            projection
            )
    response = JSONResponse(content=json.loads(json.dumps(content, indent=1, default=str)))
    if token_data['status'] == "refresh":
        response.set_cookie(key=COOKIES_KEY_NAME, value=token_data['access_token'], httponly=True)

    return response

async def get_request_dtl(request_id: str) -> JSONResponse:
    work_item = work_request_collection.find_one(ObjectId(request_id))
    response = JSONResponse(content=json.loads(json.dumps(work_item, indent=1, default=str)))

    return response

async def post_temprary(request: Request, item: WorkRequestModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    work_request_collection.insert_one(item.model_dump())

    content = {"message": "Temprary Request Created"}
    response = JSONResponse(content=content)

    return response

async def update_temprary(item: UpdateWorkRequestModel):
    work_request_collection.update_one(item)

async def update_modify_request_work(
        id: str,
        user_id: str,
        device_nm: str,
        request_title: str,
        customer_nm: str,
        request_date: str,
        work_content: str,
        file: str,
        del_yn: str
        ):
    filter = {"_id": id}
    req_data = objectCleaner.cleanObject({
        "user_id": user_id,
        "device_nm": device_nm,
        "request_title": request_title,
        "customer_nm": customer_nm,
        "request_date": request_date,
        "work_content": work_content,
        "del_yn": del_yn
        })
    work_request_collection.update_one(filter, {"$set": req_data})
    work_request_collection.update_one(filter, {"$set":{"file": file}})

async def update_recovery_request_work(
        id: str
        ):
    filter = {"_id": id}
    work_request_collection.update_one(filter, {"$set":{"delYn": "Y"}})
