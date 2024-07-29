from fastapi import APIRouter, HTTPException, status, Response, Cookie, UploadFile
from fastapi.requests import Request
from routes._path.api_paths import REQUEST, READ_REQUEST, READ_REQUEST_TEMPORARY, READ_REQUEST_DETAIL, CREATE_REQUEST, CREATE_REQUEST_TEMPORARY, UPDATE_REQUEST, UPDATE_REQUEST_TEMPORARY, DELETE_REQUEST, DELETE_REQUEST_TEMPORARY

import json

from constants import COOKIES_KEY_NAME, SESSION_TIME
from db.context import auth_collection, user_collection
from models.work_request_dto import *
from httpx import AsyncClient
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse


load_dotenv()
router = APIRouter()


class Router:
    def __init__(self):
        pass


@router.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", 'HEAD', 'PATCH'])
async def proxy(request: Request, path: str):
    backend_url = f"http://localhost:3000/api/v1/{path}"
    if request.query_params:
        backend_url += f"?{request.url.query}"

    async with AsyncClient() as client:
        method = request.method
        headers = request.headers
        req_body = await request.body()
        
        access_token_cookie = request.cookies.get(COOKIES_KEY_NAME)
        get_user_id = auth_collection.find_one({"access_token": access_token_cookie})
        
        if not get_user_id:
            response = await client.request(method, backend_url, headers=headers, content=req_body, cookies=request.cookies)
            return Response(content=response.content, status_code=response.status_code, headers=headers)
        
        get_user_role = user_collection.find_one({"_id": ObjectId(get_user_id['user_id'])})
        
        if req_body:
            body_data = json.loads(req_body.decode())
            body_data['role'] = get_user_role['role']

        else:
            body_data = {'role': get_user_role['role']}

        modified_body = json.dumps(body_data).encode('utf-8')
        response = await client.request(method, backend_url, headers=headers, content=modified_body, cookies=request.cookies)
        
        return Response(content=response.content, status_code=response.status_code, headers=headers)
