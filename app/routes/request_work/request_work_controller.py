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
        

@router.post(
        "/createRequest",
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False
        )       
async def postWorkRequest(item: WorkRequestModel):
    await request_work_service.requestWork(
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

@router.get(
        "/readRequest",
        status_code=status.HTTP_200_OK,
        response_model_by_alias=False
)
async def get_request_list(page: int, userId: str):#, token: Optional[str] = Cookie(None):
    request_list = await request_work_service.get_request_work_list(page=page, user_id=userId)
    return request_list

@router.get(
    "/readDetailRequest",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def get_request_dtl(requestId: str):#,token: Optional[str] = Cookie(None)):
    request_dtl = await request_work_service.get_request_work_dtl(request_id=requestId)
    return {"requestDtl": request_dtl}
