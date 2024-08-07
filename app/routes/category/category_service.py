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
from models.category_dto import ResponseOfUserModel, ResponseOfAdminModel
from routes._modules import list_module, response_cookie_module
from routes._modules.list_module import is_temporary
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from typing import List
from pydantic.alias_generators import to_camel

async def get_info_by_user(request: Request) -> List[dict]:
    req_data = json.loads(await request.body())
    if req_data['role'] == 'user':
        get_user = user_collection.find_one({"_id": ObjectId(req_data['tokenData']['userId'])})
        projection = { "_id": 1,"company_id": 1, "product_family": 1}     
        get_contract_by_user = contract_collection.find({"company_id": get_user['company_id']}, projection)
        content = []
        for item in get_contract_by_user:
            item['_id'] = str(item['_id'])
            model_instance = ResponseOfUserModel(**item)
            model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
            content.append(model_dict)
        response_content=json.loads(json.dumps(jsonable_encoder(content, by_alias=True), indent=1, default=str))
        
        return response_content
    
    elif req_data['role'] == 'admin' or req_data['role'] == 'system admin':
        projection = { "_id": 1, "work_type": 1, "sales_manager": 1, "company_id": 1, "contract_date": 1, "product_family": 1}
        get_contract_by_user = contract_collection.find({"sales_manager": req_data['tokenData']['userData']['name']}, projection)
        content = []
        for item in get_contract_by_user:
            item['_id'] = str(item['_id'])
            model_instance = ResponseOfAdminModel(**item)
            model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
            content.append(model_dict)
            
        return content