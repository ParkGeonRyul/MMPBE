from fastapi import APIRouter
from fastapi import status
from fastapi import Response
from fastapi import Cookie
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from routes.auth import auth_service
from constants import COOKIES_KEY_NAME

from typing import Annotated

# ----------------------------------------------------------------

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
from app.routes._path.api_paths import ApiPaths

@router.get(ApiPaths.LOGIN_WITH_MS)
async def login():
    redirect_callback = await auth_service.login()

    return redirect_callback

@router.get(ApiPaths.AUTH_CALLBACK)
async def auth_callback(request: Request) -> RedirectResponse:
    auth_code = request.query_params.get("code")
    redirect = await auth_service.auth_callback(auth_code)

    return redirect

@router.get(ApiPaths.LOGOUT, status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)

@router.get(ApiPaths.CHECK_SESSION)
async def validate(request: Request) -> JSONResponse:
    return await auth_service.validate(request)