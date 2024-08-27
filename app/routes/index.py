from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from contextvars import ContextVar

import json
import msal

from constants import COOKIES_KEY_NAME
from routes._path.main_path import MAIN_URL, API_URL
from db.context import auth_collection, user_collection, role_collection
from routes._path.api_paths import *
from routes._path.ms_paths import *
from routes.auth.auth_service import *
from models.work_request_dto import *

router = APIRouter()


current_request_status = ContextVar("current_request_status", default=None)

class Router:
    def __init__(self):
        pass

msal_app = msal.ConfidentialClientApplication(
    MS_CLIENT_ID,
    authority=MS_AUTHORITY,
    client_credential=MS_CLIENT_SECRET
)

@router.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", 'HEAD', 'PATCH'])
async def proxy(request: Request, path: str):
    req_body = await request.body()
    backend_url = f"{API_URL}{path}"
    access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)

    current_request_status.set(True)

    if request.query_params:
        backend_url += f"?{request.url.query}"

    async with AsyncClient() as client:
        method = request.method
        user_token = auth_collection.find_one({"access_token": access_token_cookie})
        if not access_token_cookie or not user_token: # 토큰 없는 경우
            if path == "auth/login" or path == "auth/oauth/callback":    
                return RedirectResponse(url=backend_url)
            
            if current_request_status.get():
                raise HTTPException(status_code=400, detail="Request is already being processed")

            return RedirectResponse(url=f"{MAIN_URL}{LOGIN_WITH_MS}")
        
        current_request_status.set(None)

        # 토큰 있고 브라우저도 토큰이 있다.
        # validate
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token_cookie}"}
        )

        if user_response.status_code == 200:
            user_data = user_response.json()
            document = {
                "sign_status": "valid",
                "userId": str(user_token['user_id']),
                "name": user_data.get("displayName"),
                "email": user_data.get("mail"),
                "jobTitle": user_data.get("jobTitle"),
                "mobilePhone": user_data.get("mobilePhone")
                }
            
            cookies_data = request.cookies

        else:  # 401
            try:
                find_user = user_collection.find_one({"_id": user_token['user_id']})
            
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))
        
            if find_user:

                reissue_token = msal_app.acquire_token_by_refresh_token(user_token["refresh_token"], scopes=["User.Read"])
                await access_token_manager(True, True, reissue_token['access_token'], reissue_token['refresh_token'], user_token['user_id'], user_token['email'])
                document = {
                    "sign_status": "refresh",
                    "userId": str(user_token['user_id']),
                    "name": find_user['user_nm'],
                    "email": find_user['email'],
                    "jobTitle": find_user['rank'],
                    "mobilePhone": find_user['mobile_contact']
                    }
                
                cookies_data = {**request.cookies, COOKIES_KEY_NAME: reissue_token['access_token']}

        get_user_info = user_collection.find_one({"_id": ObjectId(document['userId'])})
        get_role = role_collection.find_one({"_id": ObjectId(get_user_info['role'])})
                
        if req_body:
            content_type = request.headers.get("Content-Type")
            
            if content_type.startswith("multipart/form-data"):
                req_data = await request.form()
                file = req_data.get("files")
                if file and hasattr(file, 'filename') and hasattr(file, 'read') and hasattr(file, 'content_type'):
                    req_json = {key: value for key, value in req_data.items() if key != "files"}
                    file_status = {'file_name': (file.filename, await file.read(), file.content_type)}
                else:
                    req_json = {key: value for key, value in req_data.items()}
                    file_status = None

                for key, value in document.items():
                    req_json[key] = value
                    
                response_data = await client.request(method, backend_url, data=req_json, cookies=cookies_data, files=file_status)

            elif content_type == "application/json" :
                req_data = await request.body()
                response_data = await client.request(method, backend_url, content=req_data, cookies=cookies_data)

        else:
            body_data = {'role': get_role['role_nm']}
            body_data['tokenData'] = document
            modified_body = json.dumps(body_data).encode('utf-8')
            response_data = await client.request(method, backend_url, content=modified_body, cookies=cookies_data)
            
        new_token = cookies_data.get(COOKIES_KEY_NAME)
        current_request_status.set(None)
        response = Response(content=response_data.content, status_code=response_data.status_code, headers=dict(response_data.headers))
        response.set_cookie(key=COOKIES_KEY_NAME, value=new_token)
            
        return response