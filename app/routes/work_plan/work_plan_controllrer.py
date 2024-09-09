from fastapi import APIRouter, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from routes._path.api_paths import SELECT_APPROVE_WR_LIST, SELECT_PLAN, SELECT_PLAN_TEMPORARY, SELECT_PLAN_DETAIL, CREATE_PLAN, UPDATE_PLAN, UPDATE_PLAN_STATUS_ACCEPT, DELETE_PLAN, DELETE_PLAN_TEMPORARY, UPDATE_PLAN_STATUS

from routes.work_plan import work_plan_service
from models.work_plan_dto import *
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

class Router:
    def __init__(self):
        pass

@router.get(SELECT_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_plan_list(request: Request):
    return await work_plan_service.get_plan_list(request, False)

@router.get(SELECT_PLAN_DETAIL, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_plan_dtl(request: Request):
    return await work_plan_service.get_plan_dtl(request)

@router.get(SELECT_APPROVE_WR_LIST, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_approve_wr_list(request:Request):
    return await work_plan_service.get_wr_list(request)

@router.post(UPDATE_PLAN_STATUS, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_plan_status(request: Request, item: UpdatePlanStatusModel):
    return await work_plan_service.update_plan_status(request, item)

@router.post(UPDATE_PLAN_STATUS_ACCEPT, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_plan_status_accept(request: Request, item: UpdatePlanStatusAcceptModel):
    return await work_plan_service.update_plan_status_accept(request, item)
    
@router.post(CREATE_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def create_plan(request: Request) -> JSONResponse:
    req_body = await request.form()
    file = req_body.get("file_name")
    if file:
        request_data = {key: value for key, value in req_body.items() if key != "files"}
    else:
        request_data = {key: value for key, value in req_body.items()}

    return await work_plan_service.create_plan(request_data, file)

@router.put(UPDATE_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_work_plan(request: Request):
    req_body = await request.form()
    file = req_body.get("file_name")
    if file:
        request_data = {key: value for key, value in req_body.items() if key != "files"}
    else:
        request_data = {key: value for key, value in req_body.items()}

    return await work_plan_service.update_plan(request, request_data, file)

@router.put(DELETE_PLAN, status_code=status.HTTP_200_OK)
async def delete_plan(request: Request):
    try:
        return await work_plan_service.del_yn_plan(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
