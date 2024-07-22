from datetime import datetime
from datetime import timezone
from datetime import timedelta

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
import msal

from bson import ObjectId
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
from db.context import authCollection
from db.context import userCollection
from db.context import ttl_seconds
from typing import Annotated
from utils import objectCleaner
from utils.objectId_convert import objectIdConvert


load_dotenv()
router = APIRouter()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"
MS_AUTHORITY = "https://login.microsoftonline.com/common"

msal_app = msal.ConfidentialClientApplication(
    MS_CLIENT_ID,
    authority=MS_AUTHORITY,
    client_credential=MS_CLIENT_SECRET
)

@router.get("/login")
async def accessCookie(ads_id: Annotated[str | None, Cookie()] = None):
    readAccessToken = authCollection.find_one(ObjectId(ads_id))
    if ads_id == None or readAccessToken == None:
        url = msal_app.get_authorization_request_url(
            scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
            redirect_uri=MS_REDIRECT_URI
            )        
        return RedirectResponse(url)
    else:
        objectIdConvert(readAccessToken)
        async with AsyncClient() as client:
            user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {readAccessToken['accessToken']}"}
        )
        if user_response.status_code == 200:
            return {"message": "access token is valid"}
        else:
            updateAccessId = msal_app.acquire_token_by_refresh_token(readAccessToken["refreshToken"], scopes=["User.Read"])
            document = {
                "accessToken": updateAccessId["access_token"],
                "refreshToken": updateAccessId["refresh_token"]
            }

            filter = {"_id": ObjectId(ads_id)}
            authCollection.update_one(filter, {"$set": document})
            return {"message": "token has been refresh"}

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

        user_data = user_response.json()

        findUser = userCollection.find_one({"email": user_data['mail']})
        objectIdConvert(findUser)

        if findUser != None:  
            expiration_time = datetime.utcnow() + timedelta(seconds=ttl_seconds)                          

            document = {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "userId": findUser['_id'],
            "expireAt": expiration_time
            }

            authCollection.insert_one(document)

            accessId = authCollection.find_one({"accessToken": document["accessToken"]})
            objectIdConvert(accessId)
            return {"accessId": accessId['_id']}
        else:
            return {"message": "Invalid User"}

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
    return "a"