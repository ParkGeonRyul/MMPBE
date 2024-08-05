import json
import pymongo
import os

from db.context import work_request_collection, auth_collection, user_collection, contract_collection
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
from models.category_dto import ResponseModel
from routes._modules import list_module, response_cookie_module
from routes._modules.list_module import is_temprary
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import List
from pydantic.alias_generators import to_camel


async def get_info_by_user(request: Request) -> List[dict]:
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
    token_data = await auth_service.validate_token(access_token_cookie)
    get_user = user_collection.find_one({"_id": ObjectId(token_data['userId'])})
    projection = { "_id": 1,"company_id": 1, "product_family": 1, "created_at": 1}     
    get_contract_by_user = contract_collection.find({"company_id": get_user['company_id']}, projection)
    content = []
    for item in get_contract_by_user:
        item['_id'] = str(item['_id'])
        item['created_at'] = item['created_at'].isoformat()
        model_instance = ResponseModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
    response_content=json.loads(json.dumps(jsonable_encoder(content, by_alias=True), indent=1, default=str))
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)

async def get_info_by_company(request: Request) -> JSONResponse:
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
    contract_id = request.query_params.get("contractId")
    token_data = await auth_service.validate_token(access_token_cookie)
    projection = {"_id": 1, "company_id": 1, "product_family": 1, "sales_manager": 1}
    get_contract = contract_collection.find_one({"_id": ObjectId(contract_id)}, projection)
    get_contract["_id"] = str(get_contract["_id"])
    model_instance = ResponseModel(**get_contract)
    model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
    response_content=json.loads(json.dumps(jsonable_encoder(model_dict, by_alias=True), indent=1, default=str))
    
    return await response_cookie_module.set_response_cookie(token_data, response_content)