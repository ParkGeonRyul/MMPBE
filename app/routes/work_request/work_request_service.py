from fastapi import Request, Response, UploadFile
from fastapi.responses import JSONResponse

import json

from db.context import work_request_collection, contract_collection
from datetime import datetime
from bson import ObjectId
from models.work_request_dto import *
from routes._modules import list_module
from routes._modules.list_module import is_temporary
from models import work_request_dto


async def get_request_list(request: Request, is_temp: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = str(req_data['tokenData']['userId'])
    role = str(req_data['role'])
    temporary_value = await is_temporary(is_temp)

    match = {
         "wr_date": temporary_value
    }

    if role != "system admin":
        
        match['del_yn']= "N"
        
    if role == "user":

        match['customer_id'] = id
          
    projection = {"_id": 1, "wr_title": 1, "sales_representative_nm": 1, "customer_nm": 1, "company_nm": 1, "wr_date": 1, "status": 1}
    
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
    req_data = json.loads(await request.body())
    id = str(req_data['tokenData']['userId'])
    request_id = request.query_params.get("_id")
    role = str(req_data['role'])
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
        
        get_sales = contract_collection.find_one({"_id": ObjectId(contract['solution_id']),"sales_representative_nm": req_data['tokenData']['userData']['name']})

        if not get_sales:
            
            raise HTTPException(status_code=404, detail="request by contract not found")
        
    projection = {
        "_id": 1,
        "wr_title": 1,
        "company_id": 1,
        "company_nm": 1,
        "sales_representative_nm": 1,
        "customer_id": 1,
        "customer_nm": 1,
        "content": 1,
        "wr_date": 1,
        "file_path": 1,
        "status": 1,
        "status_content": 1
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

async def create_request(request: Request, item: CreateWorkRequestModel) -> JSONResponse:
    try:
        work_request_collection.insert_one(item.model_dump())

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    response_content = {"message": "Work Request Created"}

    return response_content

async def update_request(request: Request, item: UpdateWorkRequestModel) -> JSONResponse:
    request_id = request.query_params.get("_id")
    try:

        work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": item.model_dump()})
    
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
    request_id = request.query_params.get("_id")
    try:

        work_request_collection.update_one({"_id": ObjectId(request_id)}, {"$set":item.model_dump()})

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    response_content = {"message": "Status modify success"}

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
