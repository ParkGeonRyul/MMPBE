from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request
from routes._path.api_paths import CATEGORY, GET_INFO_BY_COMPANY, GET_INFO_BY_USER

import os

from datetime import datetime, timezone
from utils import formating
from routes.category import category_service
from utils import dependencies
from constants import COOKIES_KEY_NAME, SESSION_TIME
from models.work_request_dto import *
from httpx import AsyncClient
from typing import List, Optional
from dotenv import load_dotenv
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, ConfigDict

load_dotenv()
router = APIRouter()


class Router:
    def __init__(self):
        pass

@router.get(GET_INFO_BY_USER, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_info_by_user(request: Request):
       
       return await category_service.get_info_by_user(request)

@router.get(GET_INFO_BY_COMPANY, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_info_by_user(request: Request):
       
       return await category_service.get_info_by_company(request)

