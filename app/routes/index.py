from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

import json
import msal

from constants import COOKIES_KEY_NAME
from routes._path.main_path import MAIN_URL, API_URL
from routes._modules.jwt import *
from routes._path.api_paths import *
from routes._path.ms_paths import *
from routes.auth.auth_service import *
from db.context import auth_collection
from models.work_request_dto import *


router = APIRouter()

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

    if request.query_params:
        backend_url += f"?{request.url.query}"

    async with AsyncClient() as client:
        method = request.method
        token_key = await parse_token(request.cookies.get(COOKIES_KEY_NAME))
        token_valid = auth_collection.find_one({"_id": ObjectId(token_key)})
        
        if not token_valid:
            if path == "auth/login" or path == "auth/oauth/callback":
                response = await client.request(method, backend_url)
                return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
            
            # 강제로 리다이렉션하는 부분
            response = await client.request(method, f"{MAIN_URL}{LOGIN_WITH_MS}")
            
            # 리다이렉션 응답을 클라이언트에 그대로 전달
            if response.status_code in [301, 302, 307, 308]:
                redirect_url = response.headers.get("Location")
                return RedirectResponse(redirect_url, status_code=response.status_code)
            
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
        
        token_data = await validate_token(token_key)
        user_data = token_data['userData']
                
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
                
                req_json['user_id'] = token_data['userId']
                for key, value in user_data.items():
                    req_json[key] = value

                response_data = await client.request(method, backend_url, data=req_json, cookies=request.cookies, files=file_status)

            elif content_type == "application/json" :
                req_json = await request.body()
                req_json = json.loads(req_json.decode('utf-8'))
                req_json['user_id'] = token_data['userId']
                for key, value in user_data.items():
                    req_json[key] = value

                response_data = await client.request(method, backend_url, json=req_json, cookies=request.cookies)

        else:
            body_data = {'user_id': token_data['userId']}
            for key, value in user_data.items():
                body_data[key] = value
            req_json = json.dumps(body_data).encode('utf-8')
            response_data = await client.request(method, backend_url, content=req_json, cookies=request.cookies)
        
        return Response(content=response_data.content, status_code=response_data.status_code, headers=dict(response_data.headers))