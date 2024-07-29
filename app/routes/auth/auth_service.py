
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from routes._path.ms_paths import MS_AUTHORITY, MS_CLIENT_ID, MS_CLIENT_SECRET, MS_PROFILE_PHOTO, MS_REDIRECT_URI, MS_TOKEN_URL, MS_USER_INFO_URL, REDIRECT_URL_HOME
from constants import ACCESS_TOKEN_NOT_VALID, ACCESS_TOKEN_VAILD, COOKIES_KEY_NAME

import msal

from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from db.context import auth_collection, user_collection
from fastapi import Request, HTTPException, status
from bson import ObjectId
from utils.objectId_convert import objectId_convert

router = APIRouter()

msal_app = msal.ConfidentialClientApplication(
    MS_CLIENT_ID,
    authority=MS_AUTHORITY,
    client_credential=MS_CLIENT_SECRET
)

async def insert_token(access_token: str, refresh_token: str, user_id: ObjectId, email: str):
    document = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user_id,
        "email": email,
        "updated_at": datetime.now()
    }
    auth_collection.insert_one(document)
    user_token = auth_collection.find_one({"user_id": user_id})

    return user_token

async def access_token_manager(is_user:bool, check_token_existence:bool, access_token: str, refresh_token: str, user_id: ObjectId, email: str):                       
    if is_user:
        document = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "updated_at": datetime.now()
        }
        filter = {"user_id": user_id}
        if check_token_existence:
            auth_collection.update_one(filter,{"$set":document})
            user_token = auth_collection.find_one({"user_id": user_id})
 
            return user_token
        else:

            return await insert_token(access_token, refresh_token, user_id, email)
    else:
        
        return await insert_token(access_token, refresh_token, user_id, email)

async def login():
    url = msal_app.get_authorization_request_url(
        scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
        redirect_uri=MS_REDIRECT_URI
    )
    print(url)

    return RedirectResponse(url=url, status_code=307)

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
        find_token = auth_collection.find_one({"email": user_data['mail']})
        is_user = True if find_user else False
        check_token_existence = True if find_token else False

        if is_user:
            user_token = await access_token_manager(is_user, check_token_existence, access_token, refresh_token, find_user["_id"], find_user["email"])
            response = RedirectResponse(url=REDIRECT_URL_HOME)
            response.set_cookie(key=COOKIES_KEY_NAME, value=user_token['access_token'], httponly=True)

            return response
        else:
            document = {
                "user_nm": user_data['displayName'],
                "rank": user_data['jobTitle'],
                "mobile_contact": user_data['mobilePhone'],
                "email": user_data['mail'],
                "role": 1,
                "created_at": datetime.now()
            }
            create_user = user_collection.insert_one(document)
            user_token = await access_token_manager(is_user, check_token_existence, access_token, refresh_token, create_user.inserted_id, user_data['mail'])
            response = RedirectResponse(url=REDIRECT_URL_HOME)
            response.set_cookie(key=COOKIES_KEY_NAME, value=user_token['access_token'], httponly=True)

            return response

async def validate_token(access_token: str):
    user_token = auth_collection.find_one({"access_token": access_token})
    async with AsyncClient() as client:
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_token == None:

            raise HTTPException(status_code=user_response.status_code, detail=user_response.text)
        if user_response.status_code == 200:
            user_token = auth_collection.find_one({"access_token": access_token})
            user_data = user_response.json()
            document = {
                "status": "valid",
                "userId": user_token['user_id'],
                "userData": {
                    "name": user_data.get("displayName"),
                    "email": user_data.get("mail"),
                    "jobTitle": user_data.get("jobTitle"),
                    "mobilePhone": user_data.get("mobilePhone")
                }
            }

            return document
        else:
            find_user = user_collection.find_one({"_id": user_token['user_id']})
            if find_user:
                reissue_token = msal_app.acquire_token_by_refresh_token(user_token["refresh_token"], scopes=["User.Read"])
                await access_token_manager(True, True, reissue_token['access_token'], reissue_token['refresh_token'], user_token['user_id'], user_token['email'])
                document = {
                    "status": "refresh",
                    "userId": user_token['user_id'],
                    "user": {
                        "name": find_user['user_nm'],
                        "email": find_user['email'],
                        "jobTitle": find_user['rank'],
                        "mobilePhone": find_user['mobile_contact']
                    }                
                }

                return document
            else:
                RedirectResponse(url=REDIRECT_URL_HOME)

async def validate(request: Request) -> JSONResponse:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    valid_token = await validate_token(access_token)
    if valid_token['status'] == "valid":
        objectId_convert(valid_token, "userId")

        return JSONResponse(content=valid_token)
    else:
        access_token = auth_collection.find_one({"user_id": valid_token['userId']})
        response = JSONResponse(content=valid_token)
        response.set_cookie(key=COOKIES_KEY_NAME, value=valid_token['access_token'], httponly=True)

        return response

async def get_user_profile_image(request: Request) -> Response:
    access_token = request.cookies.get(COOKIES_KEY_NAME)
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with AsyncClient() as client:
        user_response = await client.get(
            MS_PROFILE_PHOTO,
            headers={"Authorization": f"Bearer {access_token}"}
        )

    if user_response.status_code != 200:
        raise HTTPException(status_code=user_response.status_code, detail="Failed to fetch user profile image")

    return Response(content=user_response.content, media_type="image/png")