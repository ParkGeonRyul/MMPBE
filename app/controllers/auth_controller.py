from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating
from services import user_service
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME

import os
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"

@router.get("/login")
def login_with_ms():
    params = {
        "client_id": MS_CLIENT_ID,
        "redirect_uri": MS_REDIRECT_URI,
        "response_type": "code",
        "scope": "User.Read",
        "response_mode": "query"
    }
    url = MS_AUTH_URL + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return RedirectResponse(url)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    async with AsyncClient() as client:
        token_response = await client.post(
            MS_TOKEN_URL,
            data={
                "client_id": MS_CLIENT_ID,
                "client_secret": MS_CLIENT_SECRET,
                "redirect_uri": MS_REDIRECT_URI,
                "code": code,
                "grant_type": "authorization_code"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=token_response.status_code, detail=token_response.text)

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_response.status_code != 200:
            raise HTTPException(status_code=user_response.status_code, detail=user_response.text)

        user_data = user_response.json()

    return user_data

@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)

@router.get("/validate")#, response_model=dto.Token)
async def check_session( req: Request, res: Response) -> JSONResponse:
    # token = req.cookies.get(COOKIES_KEY_NAME, "")
    
    # data = jwt_service.decode(token)
    # if data is None:
    #     res.delete_cookie(COOKIES_KEY_NAME)
    #     raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is invalid")
        
    # return data
    return 