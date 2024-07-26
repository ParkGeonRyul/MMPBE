from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request
from routes._path.api_paths import REQUEST, READ_REQUEST, READ_REQUEST_TEMPORARY, READ_REQUEST_DETAIL, CREATE_REQUEST, CREATE_REQUEST_TEMPORARY, UPDATE_REQUEST, UPDATE_REQUEST_TEMPORARY, DELETE_REQUEST, DELETE_REQUEST_TEMPORARY

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

@router.get(READ_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_list(request: Request):
    try:
       return await request_work_service.get_request_list(request, False)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(READ_REQUEST_TEMPORARY, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_temporary_list(request: Request):
    try:
        return await request_work_service.get_request_list(request, True)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(READ_REQUEST_DETAIL, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_request_dtl(request: Request):
    try:
        return await request_work_service.get_request_dtl(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(CREATE_REQUEST_TEMPORARY, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)       
async def create_temporary(request: Request, item: WorkRequestModel):
    try:
        return await request_work_service.create_temporary(request, item)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put(CREATE_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_temporary(request: Request, item: UpdateWorkRequestModel):
    try:
        await request_work_service.update_temporary(request, item)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(UPDATE_REQUEST, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_work_request(request: Request, item: UpdateWorkRequestModel):
    try:
        return await request_work_service.update_request(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(UPDATE_REQUEST_TEMPORARY, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_temporary(request: Request, item: UpdateWorkRequestModel):
    try:
        return await request_work_service.update_temporary(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete(DELETE_REQUEST_TEMPORARY, status_code=status.HTTP_200_OK)
async def delete_temporary(request: Request, item: DeleteRequestTempraryModel):
    try:    
        return await request_work_service.delete_temporary(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(DELETE_REQUEST, status_code=status.HTTP_200_OK)
async def delete_request(request: Request):
    try:
        return await request_work_service.del_yn_request(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
