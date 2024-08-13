import json
import pymongo
import os

from db.context import work_plan_collection, work_request_collection
from fastapi import HTTPException, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from db.context import Database
from routes.auth import auth_service
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner
from models import work_plan_dto
from models.work_plan_dto import *
from models.work_request_dto import *
from models import work_request_dto
from constants import COOKIES_KEY_NAME
from utils.objectId_convert import objectId_convert
from routes._modules import list_module, response_cookie_module
from routes._modules.list_module import is_temporary
from uuid import uuid4
from typing import List
    
async def get_plan_list(request: Request, is_temp: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = str(req_data['tokenData']['userId'])
    role = str(req_data['role'])
    temporary_value = await is_temporary(is_temp)

    if role == 'user':
        match = {
                    "acceptor_id": id,
                    "plan_date": temporary_value
                }

    elif role == 'admin' or role == 'system admin':    
        match = {
                    "user_id": id,
                    "plan_date": temporary_value
                }

    projection = {"_id": 1, "user_id": 1, "plan_title": 1, "acceptor_id": 1, "acceptor_nm": 1, "company_nm": 1,"requestor_nm":1, "plan_date": 1, "status": 1}   
    plan_list = await list_module.get_collection_list(match, work_plan_collection, projection, ResponsePlanListModel, work_plan_dto)
        
    content = {
        "total": len(plan_list),
        "list": plan_list
    }

    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def get_plan_dtl(request: Request) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = str(req_data['tokenData']['userId'])
    role = str(req_data['role'])
    plan_id = request.query_params.get("_id")

    if role == "user":
        projection = {
                        "_id": 1,
                        "user_id": 1,
                        "requestor_nm": 1,
                        "request_id": 1,
                        "wr_title": 1,
                        "acceptor_id": 1,
                        "acceptor_nm": 1,
                        "plan_title": 1,
                        "plan_content": 1,
                        "plan_date": 1,
                        "file_path": 1,
                        "status": 1,
                        "status_content": 1,
                        "updated_at": 1        
                    }
        get_plan = work_plan_collection.find_one({"_id": ObjectId(plan_id), "acceptor_id": id})        
        if not get_plan:
            
            raise HTTPException(status_code=404, detail="plan not found")
    
    elif role == "admin" or role == "system admin":
        projection = {
                        "_id": 1,
                        "user_id": 1,
                        "requestor_nm": 1,
                        "request_id": 1,
                        "wr_title": 1,
                        "company_id": 1,
                        "company_nm": 1,
                        "acceptor_id": 1,
                        "acceptor_nm": 1,
                        "plan_title": 1,
                        "plan_content": 1,
                        "plan_date": 1,
                        "file_path": 1,
                        "status": 1,
                        "status_content": 1,
                        "updated_at": 1        
                    }
        get_plan = work_plan_collection.find_one({"_id": ObjectId(plan_id), "user_id": id})
        if not get_plan:
            
            raise HTTPException(status_code=404, detail="plan not found")

    match = {
        "_id": ObjectId(plan_id)
    }
    
    plan_dtl = await list_module.get_collection_dtl(
        match,
        work_plan_collection,
        projection,
        ResponsePlanDtlModel,
        work_plan_dto
        )
    
    response_content=json.loads(json.dumps(plan_dtl, indent=1, default=str))
    
    return response_content


async def get_approve_wr_list(request: Request, is_temp: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = str(req_data['tokenData']['userId'])
    role = str(req_data['role'])
    temporary_value = await is_temporary(is_temp)

    match = {
                "wr_date": temporary_value,
                "status" : "승인"
            }
          
    projection = {"_id": 1, "wr_title": 1, "sales_representative_nm": 1, "customer_id" : 1, "customer_nm": 1, "company_nm": 1, "wr_date": 1, "status": 1}
    
    wr_list = await list_module.get_collection_list(
        match,
        work_request_collection,
        projection,
        ResponseRequestListModel,
        work_request_dto
        )
    
    content = {
        "total": len(wr_list),
        "list": wr_list
    }
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def update_plan_status(request: Request, item: UpdatePlanStatusAcceptModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    print("item ::::::::::::: ", dict(item))
    _id = request.query_params.get("_id")
    if(_id != ""):
        work_plan_collection.update_one({"_id": ObjectId(_id)}, {"$set": item.model_dump()})
        response_content = {"result": "success"}
    else:
        response_content = {"result": "fail"}
    
    return response_content

async def update_plan_status_accept(request: Request, item: UpdatePlanStatusAcceptModel) -> JSONResponse:
    _id = request.query_params.get("_id")
    if(_id != ""):
        work_plan_collection.update_one({"_id": ObjectId(_id)}, {"$set": item.model_dump()})
        response_content = {"result": "success"}
    else:
        response_content = {"result": "fail"}
    
    return response_content

async def create_plan(request: Request, item: CreateWorkPlanModel) -> JSONResponse:
    req_data = json.loads(await request.body())
    document = item.model_dump()
    document['customer_id'] = req_data['userData']['userId']
    work_plan_collection.insert_one(document)
    response_content = {"message": "Request Plan Created"}
    
    return response_content

async def create_temporary(request: Request, item: CreateWorkPlanModel) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token)
    work_plan_collection.insert_one(item.model_dump())
    response_content = {"message": "Temporary Request Created"}
    
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
