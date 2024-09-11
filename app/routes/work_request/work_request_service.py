from fastapi import Request, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from bson import ObjectId

import json
import os

from routes._modules import list_module
from routes._modules.list_module import is_temporary
from routes._modules.file_server import *
from models import work_request_dto
from models.work_request_dto import *
from db.context import work_request_collection, contract_collection

load_dotenv()

upload_path = os.getenv("UPLOAD_PATH")

async def get_request_list(request: Request, is_temp: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    req_user = request.state.user
    id = str(req_user['user_id'])
    role = str(req_user['userData']['role'])
    temporary_value = await is_temporary(is_temp)

    match = {
         "wr_date": temporary_value
    }

    if role != "system admin":
        
        match['del_yn'] = "N"
        
        if role == "user":

            match['customer_id'] = id

        elif role == 'admin':
            
            match['status'] = {"$ne" : "회수"}
            match['sales_representative_nm'] = req_data['userData']['name']
          
    projection = {"_id": 1, "wr_title": 1, "sales_representative_nm": 1, "contract_title": 1, "customer_nm": 1, "company_nm": 1, "contract_title":1, "wr_date": 1, "status": 1}
    
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

async def get_request_dtl(request: Request) -> JSONResponse:
    request_id = request.query_params.get("_id")
    req_data = json.loads(await request.body())
    req_user = request.state.user
    id = str(req_user['user_id'])
    role = str(req_user['userData']['role'])
    match = {
        "_id": ObjectId(request_id)
    }
    
    if role !="system admin":
        match["del_yn"] = "N"

    if role == "user":
        get_wr = work_request_collection.find_one({"_id": ObjectId(request_id), "customer_id": id})

        if not get_wr:            
            raise HTTPException(status_code=404, detail="request not found")
    
    elif role == "admin":
        contract = work_request_collection.find_one({"_id": ObjectId(request_id)})

        if not contract:            
            raise HTTPException(status_code=404, detail="request not found")
        
        get_sales = contract_collection.find_one({"_id": ObjectId(contract['solution_id']),"sales_representative_nm": req_data['userData']['name']})

        if not get_sales:            
            raise HTTPException(status_code=404, detail="request by contract not found")
        
    projection = {
        "_id": 1,
        "wr_title": 1,
        "solution_id": 1,
        "company_id": 1,
        "company_nm": 1,
        "sales_representative_nm": 1,
        "customer_id": 1,
        "customer_nm": 1,
        "content": 1,
        "wr_date": 1,
        "status": 1,
        "file_id": 1,
        "status_content": 1,
        "file": 1,
        }
    wr_dtl = await list_module.get_collection_dtl(
        match,
        work_request_collection,
        projection,
        ResponseRequestDtlModel,
        work_request_dto
        )
    
    response_content=json.loads(json.dumps(wr_dtl, indent=1, default=str))

    return response_content


async def create_request(item: dict, file: None | UploadFile = File(...)) -> JSONResponse:
    document = dict(CreateWorkRequestModel(**item))
    document['customer_id'] = item['user_id']

    try: 
        if file:
             file_data = await upload_file(item['user_id'], file)
             document['file_path'] = file_data['file_id']

        work_request_collection.insert_one(document)

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    
    response_content = {"message": "Work Request Created"}

    return response_content

async def update_request(request: Request, item: dict, file: None | UploadFile = File(...)) -> JSONResponse:
    document = dict(UpdateWorkRequestModel(**item))
    document['customer_id'] = item['user_id']
    try:
        if file:
             file_data = await upload_file(item['user_id'], file)
             document['file_path'] = file_data['file_id']

        work_request_collection.update_one({"_id": ObjectId(document['id'])}, {"$set": document})
    
    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    response_content = {"message": "Request Created"}

    return response_content

async def delete_request(request: Request) -> JSONResponse:
    request_id = request.query_params.get("_id")
    get_request = work_request_collection.find_one({"_id": ObjectId(request_id)})
    
    try:         
        if get_request['del_yn'] == "N":
            work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "Y"}})
        else:
            work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "N"}})
    
    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    response_content = {"message": "Request delete processing completed"}


    return response_content

async def update_request_status(request: Request, item: UpdateRequestStatusAcceptModel) -> JSONResponse:
    req_body = await request.json()
    request_id = req_body["_id"]

    try:
        work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":item.model_dump()})

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    response_content = {"message": "Status modify success"}

    return response_content
