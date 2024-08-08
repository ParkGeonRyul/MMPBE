from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request
from routes._path.api_paths import PLAN, SELECT_PLAN, SELECT_PLAN_TEMPORARY, SELECT_PLAN_DETAIL, CREATE_PLAN, CREATE_PLAN_TEMPORARY, UPDATE_PLAN, UPDATE_PLAN_TEMPORARY, DELETE_PLAN, DELETE_PLAN_TEMPORARY

import os

from datetime import datetime, timezone
from utils import formating
from routes.work_plan import work_plan_service
from utils import dependencies
from constants import COOKIES_KEY_NAME, SESSION_TIME
from models.work_plan_dto import *
from httpx import AsyncClient
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()



class Router:
    def __init__(self):
        pass

@router.get(SELECT_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_plan_list(request: Request):
            
    return await work_plan_service.get_plan_list(request, False)

@router.get(SELECT_PLAN_TEMPORARY, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_temporary_list(request: Request):
    try:
        return await work_plan_service.get_plan_list(request, True)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(SELECT_PLAN_DETAIL, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_plan_dtl(request: Request):
    return await work_plan_service.get_plan_dtl(request)

@router.post(CREATE_PLAN_TEMPORARY, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)       
async def create_temporary(request: Request, item: CreateWorkPlanModel):
    try:
        return await work_plan_service.create_temporary(request, item)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post(CREATE_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def create_plan(request: Request, item: CreateWorkPlanModel):
    return await work_plan_service.create_plan(request, item)



@router.put(UPDATE_PLAN, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_work_plan(request: Request, item: UpdateWorkPlanModel):
    try:
        return await work_plan_service.update_plan(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(UPDATE_PLAN_TEMPORARY, status_code=status.HTTP_200_OK, response_model_by_alias=False)       
async def update_temporary(request: Request, item: UpdateWorkPlanModel):
    try:
        return await work_plan_service.update_temporary(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete(DELETE_PLAN_TEMPORARY, status_code=status.HTTP_200_OK)
async def delete_temporary(request: Request, item: DeletePlanTempraryModel):
    try:    
        return await work_plan_service.delete_temporary(request, item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put(DELETE_PLAN, status_code=status.HTTP_200_OK)
async def delete_plan(request: Request):
    try:
        return await work_plan_service.del_yn_plan(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
