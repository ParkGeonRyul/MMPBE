from fastapi import APIRouter
from fastapi import status
from fastapi import Response
from fastapi import Cookie
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from routes.auth import auth_service
from constants import COOKIES_KEY_NAME

from typing import Annotated

router = APIRouter()

@router.get("/login")
async def login(ads_id: Annotated[str | None, Cookie()] = None):
    redirect_callback = await auth_service.access_cookie(ads_id)

    return redirect_callback

@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    example = await auth_service.auth_callback(code)

    return example

@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)