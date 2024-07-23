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

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"
MS_AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_URL_HOME = os.getenv("REDIRECT_URL_HOME")
# ----------------------------------------------------------------


router = APIRouter()

@router.get("/login")
async def login():
    redirect_callback = await auth_service.login()

    return redirect_callback

@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    example = await auth_service.auth_callback(code)

    return example

@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)

@router.get("/validate")
async def validate(request: Request) -> JSONResponse:
    return await auth_service.validate(request)