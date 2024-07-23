
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

msal_app = msal.ConfidentialClientApplication(
    MS_CLIENT_ID,
    authority=MS_AUTHORITY,
    client_credential=MS_CLIENT_SECRET
)

async def access_token_manager(isUser:bool, access_token: str, refresh_token: str, user_id: str, email: str):                       
    if isUser:
        document = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        filter = {"user_id": user_id}
        auth_collection.update_one(filter,{"$set":document})
        user_token = auth_collection.find_one({"user_id": user_id})

        return user_token
    else:
        document = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "email": email
        }
        auth_collection.insert_one(document)
        user_token = auth_collection.find_one({"access_token": document["access_token"]})

        return user_token

async def login():
    url = msal_app.get_authorization_request_url(
        scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
        redirect_uri=MS_REDIRECT_URI
    )        

    return RedirectResponse(url)

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
        isUser = True if find_user else False

        if find_user == None:
            document = {
                "user_nm": user_data['displayName'],
                "rank": user_data['jobTitle'],
                "mobile_contact": user_data['mobilePhone'],
                "email": user_data['mail'],
                "role": 1
            }
            create_user = user_collection.insert_one(document)
            user_token = await access_token_manager(isUser, access_token, refresh_token, create_user.inserted_id, user_data['mail'])
            response = JSONResponse(content=user_token['access_token'])
            response.set_cookie(key=COOKIES_KEY_NAME, value=user_token, httponly=True)

            return RedirectResponse(url="http://localhost:8083/dashboard")
        else:
            objectId_convert(find_user)
            user_token = await access_token_manager(isUser, access_token, refresh_token, find_user["_id"], find_user["email"])
            response = JSONResponse(content=user_token['access_token'])
            response.set_cookie(key=COOKIES_KEY_NAME, value=user_token, httponly=True)

            return RedirectResponse(url="http://localhost:8083/dashboard")
        
# @router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
# async def logout(res: Response) -> JSONResponse:
#     res.delete_cookie(COOKIES_KEY_NAME) 


@router.get("/validate")
async def validate(request: Request) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    if access_token:
        async with AsyncClient() as client:
            user_response = await client.get(
                MS_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if user_response.status_code == 200:
                user_data = user_response.json()
                res_content = {
                    "message": "access token is valid",
                    "user": {
                        "name": user_data.get("displayName"),
                        "email": user_data.get("mail"),
                        "jobTitle": user_data.get("jobTitle"),
                        "mobilePhone": user_data.get("mobilePhone")
                    }
                }
                return JSONResponse(content=res_content)
            else:
                res_content = {"message": "access token is invalid"}
                return JSONResponse(content=res_content, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        res_content = {"message": "access token not found"}
        return JSONResponse(content=res_content, status_code=status.HTTP_401_UNAUTHORIZED)