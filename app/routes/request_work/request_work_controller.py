from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request

import os

from datetime import datetime, timezone
from utils import formating
from routes.request_work import request_work_service
from utils import dependencies
from constants import COOKIES_KEY_NAME, SESSION_TIME
from models.work_request_dto import *
from httpx import AsyncClient
from typing import List, Optional
from dotenv import load_dotenv


load_dotenv()
router = APIRouter()


class Router:
    def __init__(self):
        pass

@router.get("/readRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_list(request: Request):
   
   return await request_work_service.get_request_list(request, False)

@router.get("/readRequestTemprary", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_list(request: Request):

    return await request_work_service.get_request_list(request, True)

@router.get("/readDetailRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_dtl(request: Request):
    
    return await request_work_service.get_request_dtl(request)

@router.post("/createTemprary", status_code=status.HTTP_201_CREATED, response_model_by_alias=False)       
async def post_temprary(request: Request, item: WorkRequestModel):
    try:
        return await request_work_service.post_temprary(request, item)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/updateTemprary", status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_temprary(request: Request, item: UpdateWorkRequestModel):
    try:
        await request_work_service.update_temprary(request, item)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/updateRequest", status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_work_request(request: Request, item: UpdateWorkRequestModel):
    
    return await request_work_service.update_request(request, item)

@router.delete("/deleteTemprary", status_code=status.HTTP_200_OK)
async def delete_temprary(request: Request, item: DeleteRequestTempraryModel):
    
    return await request_work_service.delete_temprary(request, item)

@router.put("/deleteRequest", status_code=status.HTTP_200_OK)
async def delete_request(request: Request):
    
    return await request_work_service.del_yn_request(request)
# @router.get(
#     "/readDetailTemprary",
#     status_code=status.HTTP_200_OK,
#     response_model_by_alias=False
# )
# async def get_request_dtl(requestId: str):
#     temprary_dtl = await request_work_service.get_request_dtl(requestId, True)
    
    # return temprary_dtl