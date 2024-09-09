from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from routes._path.api_paths import READ_REQUEST, READ_REQUEST_TEMPORARY, READ_REQUEST_DETAIL, CREATE_REQUEST, UPDATE_REQUEST, DELETE_REQUEST, UPDATE_REQUEST_STATUS, CATEGORY
from routes.work_request import work_request_service
from models.work_request_dto import *


router = APIRouter()

class Router:
    def __init__(self):
        pass

@router.get(READ_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def get_request_list(request: Request) -> JSONResponse:
       
    return await work_request_service.get_request_list(request, False)

@router.get(READ_REQUEST_TEMPORARY, status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def get_temporary_list(request: Request) -> JSONResponse:
        
    return await work_request_service.get_request_list(request, True)

@router.get(READ_REQUEST_DETAIL, status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def get_request_dtl(request: Request, _id: str = Query(...)) -> JSONResponse:

    return await work_request_service.get_request_dtl(request)

@router.get(CATEGORY, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_category(request: Request):
       
       return await work_request_service.get_wr_list(request)

@router.post(CREATE_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def create_request(request: Request) -> JSONResponse:
    req_body = await request.form()
    file = req_body.get("file_name")
    if file:
        request_data = {key: value for key, value in req_body.items() if key != "files"}
    else:
        request_data = {key: value for key, value in req_body.items()}

    return await work_request_service.create_request(request_data, file)

@router.put(UPDATE_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_work_request(request: Request):
    req_body = await request.form()
    file = req_body.get("file_name")
    if file:
        request_data = {key: value for key, value in req_body.items() if key != "files"}
    else:
        request_data = dict(req_body)

    return await work_request_service.update_request(request, request_data, file)

@router.put(DELETE_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def delete_work_request(request: Request):

    return await work_request_service.delete_request(request)

@router.put(UPDATE_REQUEST_STATUS, status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def update_request_status(request: Request, item: UpdateRequestStatusAcceptModel):

    return await work_request_service.update_request_status(request, item)