from fastapi import APIRouter, HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request

import os

from datetime import datetime, timezone
from utils import formating
from routes.request_work import request_work_service
from utils import dependencies
from constants import COOKIES_KEY_NAME, SESSION_TIME
from models.work_request_dto import WorkRequestModel, UpdateWorkRequestModel
from httpx import AsyncClient
from typing import List, Optional

from dotenv import load_dotenv

from modules.custom_error import testId


load_dotenv()
router = APIRouter()

class Router:
    def __init__(self):
        pass

@router.get("/readRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_list(request: Request):
    request_list = await request_work_service.get_request_list(request, False)

    return request_list

@router.get("/readRequestTemprary", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_list(request: Request):
    temprary_list = await request_work_service.get_request_list(request, True)

    return temprary_list

@router.get("/readDetailRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_dtl(requestId: str):
    request_dtl = await request_work_service.get_request_dtl(requestId)
    
    return request_dtl

@router.post("/createTemprary", status_code=status.HTTP_201_CREATED, response_model_by_alias=False)       
async def post_temprary(request: Request, item: WorkRequestModel):
    try:
        
        return await request_work_service.post_temprary(request, item)
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/updateTemprary", status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def post_work_request(request: Request):
    try:
        await request_work_service.post_temprary(request, request.items)

        return {"message": "Temprary Request Created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(
        "/createRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def post_work_request(item: UpdateWorkRequestModel):
    await request_work_service.post_request(item)

    return {"message": "Request Created"}

@router.put(
    "/updateRequest/modify",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def update_modify_work_request(item: UpdateWorkRequestModel):
    await request_work_service.update_modify_request_work(
        id=item.id,
        userId=item.userId,
        deviceNm=item.deviceNm,
        requestTitle=item.requestTitle,
        customerNm=item.customerNm,
        requestDt=item.requestDt,
        workContent=item.workContent,
        file=item.file
        )

    return {"message": "Request Create"}

@router.put(
    "/modify-work",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def updateModifyWorkRequest(item: UpdateWorkRequestModel):
    await request_work_service.updateModifyRequestWork(
        id=item.id,
        userId=item.userId,
        deviceNm=item.deviceNm,
        requestTitle=item.requestTitle,
        customerNm=item.customerNm,
        requestDt=item.requestDt,
        workContent=item.workContent,
        file=item.file
    )

    return {"message": "Request Updated"}

@router.put(
    "/updateRequest/delete",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def update_delete_work_request(item: UpdateWorkRequestModel):
    await request_work_service.update_recovery_request_work(
        id=item.id
    )

    return {"message": "Request Changed"}



# @router.get(
#     "/readDetailTemprary",
#     status_code=status.HTTP_200_OK,
#     response_model_by_alias=False
# )
# async def get_request_dtl(requestId: str):
#     temprary_dtl = await request_work_service.get_request_dtl(requestId, True)
    
    # return temprary_dtl