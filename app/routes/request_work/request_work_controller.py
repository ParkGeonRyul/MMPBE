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
from models.work_request_dto import WorkRequestModel

import os
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv

from modules.custom_error import testId


load_dotenv()
router = APIRouter()

@router.post(
        "/request-work",
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