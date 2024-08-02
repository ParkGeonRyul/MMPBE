from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from routes._path.api_paths import *
from routes._path.ms_paths import *

import json
import msal
import logging

from fastapi.responses import JSONResponse
from constants import COOKIES_KEY_NAME, SESSION_TIME
from db.context import auth_collection, user_collection, role_collection
from models.work_request_dto import *
from httpx import AsyncClient
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse


load_dotenv()
router = APIRouter()


class Router:
    def __init__(self):
        pass

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


@router.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", 'HEAD', 'PATCH'])
async def proxy(request: Request, path: str):
    backend_url = f"http://localhost:8000/proxy/v1/{path}"
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
    if request.query_params:
        backend_url += f"?{request.url.query}"

    async with AsyncClient() as client:
        method = request.method
        headers = request.headers
        req_body = await request.body()
        if not access_token_cookie:
            return RedirectResponse(url=backend_url)

        user_token = auth_collection.find_one({"access_token": access_token_cookie})
        if not user_token:
            return RedirectResponse(url=f"http://localhost:8000{LOGIN_WITH_MS}")

        # validate
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token_cookie}"}
        )

        if user_response.status_code == 200:
            user_data = user_response.json()
            document = {
                "status": "valid",
                "userId": str(user_token['user_id']),
                "userData": {
                    "name": user_data.get("displayName"),
                    "email": user_data.get("mail"),
                    "jobTitle": user_data.get("jobTitle"),
                    "mobilePhone": user_data.get("mobilePhone")
                }
            }

            get_user_info = user_collection.find_one({"_id": ObjectId(document['userId'])})
            get_role = role_collection.find_one({"_id": ObjectId(get_user_info['role'])})
            
            if req_body:
                response = await client.request(method, backend_url, headers=headers, content=req_body, cookies=request.cookies)
                
                return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

            else:
                body_data = {'role': get_role['role_nm']}
                body_data['tokenData'] = document

            modified_body = json.dumps(body_data).encode('utf-8')
            response = await client.request(method, backend_url, headers=headers, content=modified_body, cookies=request.cookies)
            
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
            
        else:            
            find_user = user_collection.find_one({"_id": user_token['user_id']})
            if find_user:
                reissue_token = msal_app.acquire_token_by_refresh_token(user_token["refresh_token"], scopes=["User.Read"])
                await access_token_manager(True, True, reissue_token['access_token'], reissue_token['refresh_token'], user_token['user_id'], user_token['email'])
                document = {
                    "status": "refresh",
                    "userId": str(user_token['user_id']),
                    "user": {
                        "name": find_user['user_nm'],
                        "email": find_user['email'],
                        "jobTitle": find_user['rank'],
                        "mobilePhone": find_user['mobile_contact']
                    }                
                }

                get_user_info = user_collection.find_one({"_id": ObjectId(document['userId'])})
                get_role = role_collection.find_one({"_id": ObjectId(get_user_info['role'])})
                
                if req_body:
                    body_data = json.loads(req_body.decode())
                    body_data['role'] = get_role['role']
                    body_data['tokenData'] = document

                else:
                    body_data = {'role': get_role['role']}
                    body_data['tokenData'] = document

                modified_body = json.dumps(body_data).encode('utf-8')
                response = await client.request(method, backend_url, headers=headers, content=modified_body, cookies=request.cookies)
                
                return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
            
            else:
                RedirectResponse(f"http://localhost:8083/")