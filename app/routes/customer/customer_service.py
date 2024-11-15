from fastapi import Request
from fastapi.responses import JSONResponse
from bson import ObjectId

import json

from db.context import user_collection
from models.user_dto import *
from routes._modules import list_module
from models import user_dto

async def get_customer_list() -> JSONResponse:
    match = {
        "role" : '66a83425be3a5f7919351fc1'
    }
    projection = {"_id": 1, "company_nm": 1, "user_nm": 1, "mobile_contact":1, "email": 1, "created_at": 1, "del_yn": 1}
    
    customer_list = await list_module.get_collection_list(
        match,
        user_collection,
        projection,
        ResponseUserListModel,
        user_dto
        )
    
    content = {
        "total": len(customer_list),
        "list": customer_list
    }
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def get_customer_detail(request: Request) -> JSONResponse:
    user_id = request.query_params.get("_id")
    match = {
        "_id": ObjectId(user_id)
    }
    projection = {
        "_id" : 1,
        "company_id" : 1,
        "company_nm" : 1,
        "user_nm" : 1,
        "image" : 1,
        "rank" : 1,
        "company_contact" : 1,
        "mobile_contact" : 1,
        "email" : 1,
        "responsible_party" : 1,
        "role" : 1,
        "created_at" : 1,
        "del_yn" : 1
    }
    plan_dtl = await list_module.get_collection_dtl(
        match,
        user_collection,
        projection,
        ResponseUserDtlModel,
        user_dto
        )
    response_content=json.loads(json.dumps(plan_dtl, indent=1, default=str))
    
    return response_content
