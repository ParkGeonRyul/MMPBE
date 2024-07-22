from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating, dependencies
from routes.user import user_service
from constants import COOKIES_KEY_NAME, SESSION_TIME

import json
import pymongo
import os
import msal

from bson import ObjectId
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
from db.context import auth_collection, user_collection
from typing import Annotated
from utils import objectCleaner
from utils.objectId_convert import objectId_convert

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

async def get_access_id(
        access_token: str, 
        refresh_token: str, 
        user_id: str, 
        email: str
        ):                       
    document = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user_id,
        "email": email
    }
    auth_collection.insert_one(document)
    access_token = auth_collection.find_one({"access_token": document["access_token"]})
    objectId_convert(access_token)
    
    return access_token

async def access_cookie(ads_id):
    if ads_id == None:
        url = msal_app.get_authorization_request_url(
            scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
            redirect_uri=MS_REDIRECT_URI
        )        

        return RedirectResponse(url)
    else:
        async with AsyncClient() as client:
            user_response = await client.get(
                MS_USER_INFO_URL,
                headers={"Authorization": f"Bearer {ads_id}"}
            )
            if user_response.status_code == 200:
                res_content = {"message": "access token is valid"}
                response = JSONResponse(content=res_content)
                response.set_cookie(key=COOKIES_KEY_NAME, value=ads_id, httponly=True)

                return response
            else:
                read_access_token = auth_collection.find_one({"access_token": ads_id})
                objectId_convert(read_access_token)
                update_access_id = msal_app.acquire_token_by_refresh_token(read_access_token["refresh_token"], scopes=["User.Read"])
                document = {
                    "access_token": update_access_id["access_token"],
                    "refresh_token": update_access_id["refresh_token"]
                }

                filter = {"access_token": ads_id}
                auth_collection.update_one(filter, {"$set": document})

                res_content = {"message": "access token is valid"}
                response = JSONResponse(content=res_content)
                response.set_cookie(key=COOKIES_KEY_NAME, value=document['access_token'], httponly=True)

                return response

async def auth_callback(code):
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

        find_user = user_collection.find_one({"email": user_data['mail']})

        if find_user == None:
            document = {
                "user_nm": user_data['displayName'],
                "rank": user_data['jobTitle'],
                "mobile_contact": user_data['mobilePhone'],
                "email": user_data['mail'],
                "role": 1
            }

            create_user = user_collection.insert_one(document)
            access_user = await get_access_id(access_token, refresh_token, create_user.inserted_id, user_data['mail'])
            
            res_content = {"message": "access token created"}
            response = JSONResponse(content=res_content)
            response.set_cookie(key=COOKIES_KEY_NAME, value=access_user['access_token'], httponly=True)
            return response
        else:
            objectId_convert(find_user)
            access_user = await get_access_id(access_token, refresh_token, find_user["_id"], find_user["email"])
            
            res_content = {"message": "access token created"}
            response = JSONResponse(content=res_content)
            response.set_cookie(key=COOKIES_KEY_NAME, value=access_user['access_token'], httponly=True)
            return response

@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)