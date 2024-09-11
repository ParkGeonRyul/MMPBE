from fastapi import HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse
from bson import ObjectId

import json

from db.context import work_plan_collection
from models.work_plan_dto import *
from routes._modules.list_module import is_temporary
from routes._modules.file_server import *
from routes._modules.mongo_join import *


async def get_plan_list(request: Request, is_temp: bool) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = str(req_data['user_id'])
    role = str(req_data['role'])
    skip = int(request.query_params.get("page"))
    limit = int(request.query_params.get("limit"))
    temporary_value = await is_temporary(is_temp)
    
    match = {
        "plan_date": temporary_value,
    }

    if role != "system admin":
        
        match['del_yn']= "N"
        
        if role == "user":

            match['acceptor_id'] = id
            match['status'] = {"$ne" : "회수"}
            
        if role == "admin":

            match['user_id'] = id

    projection = {"_id": 1, "user_id": 1, "plan_title": 1, "acceptor_id": 1, "acceptor_nm": 1, "company_nm": 1, "wr_title": 1, "requestor_nm":1, "plan_date": 1, "status": 1}   
    plan_list = await get_list(match, projection, skip, limit)
        
    content = {
        "total": len(plan_list),
        "list": plan_list
    }

    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def get_plan_dtl(request: Request) -> JSONResponse:
    req_data = json.loads(await request.body())
    id = req_data['user_id']
    role = req_data['role']
    plan_id = request.query_params.get("_id")
    match = {
                "_id": ObjectId(plan_id)
            }
    projection = {
                    "_id": 1,
                    "user_id": 1,
                    "request_id": 1,
                    'requestor_data': 1,
                    'company_id': 1,
                    "company_nm": 1,
                    'acceptor_data': 1,
                    "wr_title": 1,
                    "plan_title": 1,
                    "plan_content": 1,
                    "plan_date": 1,
                    "files": 1,
                    "status": 1,
                    "status_content": 1,
                    "updated_at": 1        
                }

    if role != "system admin":
        match['del_yn'] = "N"

        if role == "user":            
            del projection['company_id']
            del projection['company_nm']
            match['acceptor_id'] = id
        
        elif role == "admin":

            match['user_id'] = id
    
    plan_dtl = await get_dtl(
        match,
        projection
        )
    
    response_content=json.loads(json.dumps(plan_dtl, indent=1, default=str))
    
    return response_content


async def get_wr_list(request: Request) -> JSONResponse:
    match = {
                "status" : "승인"
            }
          
    projection = {"_id": 1, "wr_title": 1, "sales_representative_nm": 1, "customer_id" : 1, "customer_nm": 1, "company_nm": 1, "wr_date": 1, "status": 1}
    
    wr_list = await get_category_list(
        match,
        projection
        )
    
    content = {
        "total": len(wr_list),
        "list": wr_list
    }
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def update_plan_status(request: Request, item: UpdatePlanStatusAcceptModel) -> JSONResponse:
    req_body = await request.json()
    plan_id = req_body['id']
    if(plan_id != ""):
        work_plan_collection.update_one({"_id": ObjectId(plan_id)}, {"$set": item.model_dump()})
        response_content = {"result": "success"}
    else:
        response_content = {"result": "fail"}
    
    return response_content

async def update_plan_status_accept(request: Request, item: UpdatePlanStatusAcceptModel) -> JSONResponse:
    req_body = await request.json()
    plan_id = req_body['id']
    if(plan_id != ""):
        work_plan_collection.update_one({"_id": ObjectId(plan_id)}, {"$set": item.model_dump()})
        response_content = {"result": "success"}
    else:
        response_content = {"result": "fail"}
    
    return response_content

async def create_plan(item: dict, file: None | UploadFile = File(...)) -> JSONResponse:
    document = dict(CreateWorkPlanModel(**item))
    document['user_id'] = item['user_id']

    try: 
        if file:
             file_data = await upload_file(item['userId'], file)
             document['file_path'] = file_data['file_id']

        work_plan_collection.insert_one(document)

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    
    response_content = {"message": "Request Plan Created"}
    
    return response_content

async def update_plan(request: Request, item: dict, file: None | UploadFile = File(...)) -> JSONResponse:
    plan_id = item['id']
    document = dict(UpdateWorkPlanModel(**item))
    document['user_id'] = item['user_id']

    try: 
        if file:
             file_data = await upload_file(item['userId'], file)
             document['file_path'] = file_data['file_id']

        work_plan_collection.update_one({"_id": ObjectId(plan_id)}, {"$set": document})

    except Exception as e:
            
            raise HTTPException(status_code=500, detail=str(e))
    
    response_content = {"message": "Request Plan Updated"}

    return response_content

async def delete_temporary(request: Request, item: DeletePlanTempraryModel):
    object_ids = [ObjectId(id) for id in item]
    work_plan_collection.delete_many({"_id": {"$in": object_ids}})
    response_content = {"message": "Temporary Deleted"}

    return response_content

async def del_yn_plan(request: Request):
    req_body = await request.json()
    request_id = req_body['id']
    test = work_plan_collection.find_one({"_id": ObjectId(request_id)})
    if test['del_yn'] == "N":
        work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "Y"}})
    else:
        work_plan_collection.update_one({"_id": ObjectId(request_id)}, {"$set":{"del_yn": "N"}})

    response_content = {"message": "Plan delete processing completed"}

    return response_content
