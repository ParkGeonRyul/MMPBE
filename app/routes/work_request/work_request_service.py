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
from routes._modules.list_module import is_temporary
from models import work_request_dto
from uuid import uuid4
from typing import List


async def get_request_list(request: Request, value: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    if value == False:
        projection = {"_id": 1, "request_title": 1, "sales_representative_nm": 1, "request_date": 1, "status": 1}
    else:
        projection = {"_id": 1, "request_title": 1, "sales_representative_nm": 1, "status": 1}
    id = str(req_data['tokenData']['userId'])
    temporary_value = await is_temporary(value)
    total = {"customer_id": id, "request_date": temporary_value}
    content = await list_module.get_collection_list(
        id,
        total,
        work_request_collection,
        temporary_value,
        # int(request.query_params.get("page")),
        projection,
        ResponseRequestListModel,
        work_request_dto
        )
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content
    # _id: string; // _id
    # wrTitle: string; 
    # companyId: string;
    # customerNm: string;
    # customerId: string
    # content: string;
    # wrDate: IDateValue
    # filePath: string;
    # status: "승인" | "반려" | "요청" | "회수";
    # statusContent: string;

async def get_request_dtl(request: Request) -> JSONResponse:
    req_data = json.loads(await request.body())
    projection = {"_id": 1, "wr_title": 1, "company_id": 1, "customer_id": 1, "content":1, "wr_date": 1, "status": 1}
    request_id = request.query_params.get("_id")
    work_item = work_request_collection.find_one(ObjectId(request_id))
    response_content=json.loads(json.dumps(work_item, indent=1, default=str))
    
    return response_content

async def create_request(request: Request, item: CreateWorkRequestModel) -> JSONResponse:
    work_request_collection.insert_one(item.model_dump())
    response_content = {"message": "Work Request Created"}

    return response_content

async def update_request(request: Request, item: UpdateWorkRequestModel) -> JSONResponse:
    request_id = request.query_params.get("requestId")
    item['created_at'] = datetime.now()
    work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    response_content = {"message": "Request Created"}

    return response_content

# async def create_temporary(request: Request, item: CreateWorkRequestModel) -> JSONResponse:
#     work_request_collection.insert_one(item.model_dump())
#     response_content = {"message": "Temporary Request Created"}

#     return response_content

# async def update_temporary(request: Request, item: UpdateWorkRequestModel) -> JSONResponse:
#     request_id = request.query_params.get("requestId")
#     work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
#     response_content = {"message": "Temporary Request Updated"}

#     return response_content

# async def delete_temporary(request: Request, item: DeleteRequestTempraryModel):
#     object_ids = [ObjectId(id) for id in item]
#     work_request_collection.delete_many({"_id": {"$in": object_ids}})
#     response_content = {"message": "Temporary Deleted"}

#     return response_content

# async def del_yn_request(request: Request):
#     request_id = request.query_params.get("requestId")
#     test = work_request_collection.find_one({"_id": ObjectId(request_id)})
#     if test['del_yn'] == "N":
#         work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "Y"}})
#     else:
#         work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "N"}})

#     response_content = {"message": "Request delete processing completed"}

#     return response_content
