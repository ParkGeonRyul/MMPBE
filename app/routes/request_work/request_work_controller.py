from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating
from routes.request_work import request_work_service
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME
from models.work_request_dto import workRequestModel, updateWorkRequestModel

import os
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv

from modules.custom_error import testId


load_dotenv()
router = APIRouter()

@router.post(
        "/create-work",
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False
        )       
async def postWorkRequest(item: workRequestModel):
    await request_work_service.postRequestWork(
        userId=item.userId,
        deviceNm=item.deviceNm,
        requestTitle=item.requestTitle,
        customerNm=item.customerNm,
        requestDt=item.requestDt,
        workContent=item.workContent,
        file=item.file,
        delYn=item.delYn
        )

    return {"message": "Request Create"}

@router.put(
    "/modify-work",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def updateModifyWorkRequest(item: updateWorkRequestModel):
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
    return {"message": "Request Update"}

@router.put(
    "/recovery-work",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False
)
async def updateRecoveryWorkRequest(item: updateWorkRequestModel):
    await request_work_service.updateRecoveryRequestWork(
        id=item.id
    )
    return {"message": "Request Change"}


@router.post(
    "/test",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False)
async def testDrive(item: workRequestModel):
    test = await request_work_service.testDrive(
        item = item
    )

    return test