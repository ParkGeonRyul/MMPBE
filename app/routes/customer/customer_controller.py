from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi import HTTPException

from routes.customer import customer_service
from utils import dependencies
from models.user_dto import UserModel
from routes.customer import customer_service
from routes._path.api_paths import SELECT_CUSTOMER, SELECT_CUSTOMER_DETAIL
# -------------------------------------------------

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from constants import COOKIES_KEY_NAME

import os
import msal

from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
from db.context import auth_collection, user_collection
from utils.objectId_convert import objectId_convert
from fastapi import Request, HTTPException, status

load_dotenv()
router = APIRouter()

@router.get(SELECT_CUSTOMER)
async def get_customer(request: Request):
    return await customer_service.get_customer_list(request)

@router.get(SELECT_CUSTOMER_DETAIL)
async def get_customer(request: Request):
    return await customer_service.get_customer_detail(request)