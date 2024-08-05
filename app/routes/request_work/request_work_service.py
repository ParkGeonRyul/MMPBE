import json
import pymongo
import os

from db.context import work_request_collection, auth_collection, user_collection
from fastapi import Request, Response, UploadFile
from fastapi.responses import JSONResponse
from db.context import Database
from routes.auth import auth_service
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner
from models.work_request_dto import *
from constants import COOKIES_KEY_NAME
from utils.objectId_convert import objectId_convert
from routes._modules import list_module, response_cookie_module
from routes._modules.list_module import is_temprary
from uuid import uuid4
from typing import List


async def get_request_list(request: Request, value: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    projection = {"_id": 1, "user_id": 1, "request_title": 1, "customer_nm": 1, "request_date": 1, 'created_at': 1, 'updated_at': 1, "del_yn": 1}     
    content = await list_module.get_collection_list(
    str(req_data['tokenData']['userId']), work_request_collection, await is_temprary(value),int(request.query_params.get("page")), projection)
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def get_request_dtl(request: Request) -> JSONResponse:
    req_data = json.loads(await request.body())
    request_id = request.query_params.get("requestId")
    work_item = work_request_collection.find_one(ObjectId(request_id))
    response_content=json.loads(json.dumps(work_item, indent=1, default=str))
    
    return response_content

async def create_temporary(request: Request, item: CreateWorkRequestModel) -> JSONResponse:
    work_request_collection.insert_one(item.model_dump())
    response_content = {"message": "Temporary Request Created"}

    return response_content

async def update_temporary(request: Request, item: UpdateWorkRequestModel) -> JSONResponse:
    request_id = request.query_params.get("requestId")
    work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    response_content = {"message": "Temporary Request Updated"}

    return response_content

async def update_request(request: Request, item: UpdateWorkRequestModel) -> JSONResponse:
    request_id = request.query_params.get("requestId")
    item['created_at'] = datetime.now()
    work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    response_content = {"message": "Request Created"}

    return response_content

async def delete_temporary(request: Request, item: DeleteRequestTempraryModel):
    object_ids = [ObjectId(id) for id in item]
    work_request_collection.delete_many({"_id": {"$in": object_ids}})
    response_content = {"message": "Temporary Deleted"}

    return response_content

async def del_yn_request(request: Request):
    request_id = request.query_params.get("requestId")
    test = work_request_collection.find_one({"_id": ObjectId(request_id)})
    if test['del_yn'] == "N":
        work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "Y"}})
    else:
        work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "N"}})

    response_content = {"message": "Request delete processing completed"}

    return response_content
