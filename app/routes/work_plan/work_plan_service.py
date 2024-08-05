import json
import pymongo
import os

from db.context import work_plan_collection, auth_collection, user_collection
from fastapi import HTTPException, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from db.context import Database
from routes.auth import auth_service
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner
from models.work_plan_dto import *
from constants import COOKIES_KEY_NAME
from utils.objectId_convert import objectId_convert
from routes._modules import list_module, response_cookie_module
from routes._modules.list_module import is_temprary
from uuid import uuid4
from typing import List


async def get_plan_list(request: Request, value: bool) -> JSONResponse:
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token_cookie)
    projection = {"_id": 1, "user_id": 1, "request_title": 1, "customer_nm": 1, "request_date": 1, 'created_at': 1, 'updated_at': 1, "del_yn": 1}     
    content = await list_module.get_collection_list(
    str(token_data['userId']), work_plan_collection, await is_temprary(value),int(request.query_params.get("page")), projection)
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def get_plan_dtl(request: Request) -> JSONResponse:
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token_cookie)
    request_id = request.query_params.get("requestId")
    work_item = work_plan_collection.find_one(ObjectId(request_id))
    response_content=json.loads(json.dumps(work_item, indent=1, default=str))
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def create_temporary(request: Request, item: CreateWorkPlanModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    work_plan_collection.insert_one(item.model_dump())
    response_content = {"message": "Temporary Request Created"}
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def create_plan(request: Request, item: CreateWorkPlanModel) -> JSONResponse:
    print(item)
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    print(access_token)
    work_plan_collection.insert_one(item.model_dump())
    response_content = {"message": "Request Plan Created"}
    print(work_plan_collection.count_documents + " ::::::::::::: service 확인" )
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def update_temporary(request: Request, item: UpdateWorkPlanModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    request_id = request.query_params.get("requestId")
    token_data = await auth_service.validate_token(access_token)
    work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    response_content = {"message": "Temporary Request Updated"}

    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def update_plan(request: Request, item: UpdateWorkPlanModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    request_id = request.query_params.get("requestId")
    token_data = await auth_service.validate_token(access_token)
    item['created_at'] = datetime.now()
    work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    response_content = {"message": "Request Created"}

    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def delete_temporary(request: Request, item: DeletePlanTempraryModel):
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    object_ids = [ObjectId(id) for id in item]
    work_plan_collection.delete_many({"_id": {"$in": object_ids}})
    response_content = {"message": "Temporary Deleted"}

    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def del_yn_plan(request: Request):
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    request_id = request.query_params.get("requestId")
    test = work_plan_collection.find_one({"_id": ObjectId(request_id)})
    if test['del_yn'] == "N":
        work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "Y"}})
    else:
        work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "N"}})

    response_content = {"message": "Request delete processing completed"}

    return await response_cookie_module.set_response_cookie(token_data, response_content)
