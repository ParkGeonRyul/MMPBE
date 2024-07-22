from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import Cookie
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating
from routes.user import user_service
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME

import json
import pymongo
import os
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
from db.context import authCollection
from typing import Annotated

load_dotenv()
router = APIRouter()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"

@router.get("/login")
async def accessCookie(ads_id: Annotated[str | None, Cookie()] = None):
    if ads_id == None:
        params = {
            "client_id": MS_CLIENT_ID,
            "redirect_uri": MS_REDIRECT_URI,
            "response_type": "code",
            "scope": "https%3A%2F%2Fgraph.microsoft.com%2F.default%20offline_access",
            "response_mode": "query"
        }
        url = MS_AUTH_URL + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        return RedirectResponse(url)
    else:
        params = {
            "client_id": MS_CLIENT_ID
        }
        test = authCollection.find_one({ "accessToken": ads_id })
        if test:
            test['_id'] = str(test['_id'])


        async with AsyncClient() as client:
            user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {test['accessToken']}"}
        )
        
        if user_response.status_code == 200:
            return True
        else:
            async with AsyncClient() as client:
                accessToken = await client.get(
                    MS_TOKEN_URL,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    data={
                        "client_id": MS_CLIENT_ID,
                        "scope": "User.Read",
                        "refresh_token": test['refreshToken'],
                        "grant_type": "refresh_token",
                        "client_secret": MS_CLIENT_SECRET
                        }
                )
                return accessToken
        # # if test:
        #     test['_id'] = str(test['_id'])
        #     return json.dumps(test)

# @router.get("/testt")
# def login_with_ms():
#     params = {
#         "client_id": MS_CLIENT_ID,
#         "redirect_uri": MS_REDIRECT_URI,
#         "response_type": "code",
#         "scope": "User.Read",
#         "response_mode": "query"
#     }
#     url = MS_AUTH_URL + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
#     return RedirectResponse(url)

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
                'scope': 'https://graph.microsoft.com/.default offline_access',
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
        refresh_token = token_data.get("refresh_token")
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_response.status_code != 200:
            raise HTTPException(status_code=user_response.status_code, detail=user_response.text)
        
        document = {
        "accessToken": access_token,
        "refreshToken": refresh_token
        }

        authCollection.insert_one(document)

        user_data = user_response.json()

    return token_data

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