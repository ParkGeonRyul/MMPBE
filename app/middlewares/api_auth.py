from fastapi import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from routes._path.ms_paths import *
from routes._path.api_paths import *
from routes._path.main_path import MAIN_URL, API_URL
from constants import COOKIES_KEY_NAME
from routes._modules.jwt import *
from routes.auth.auth_service import *
from db.context import auth_collection
from models.work_request_dto import *

class get_user(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        token = request.cookies.get(COOKIES_KEY_NAME)
        token_key = await parse_token(token)
        token_valid = auth_collection.find_one({"_id": ObjectId(token_key)})

        if not token or not token_valid:
            if path == "/v1/auth/login" or path == "/vi/auth/callback":
                return await call_next(request)
            
            return RedirectResponse(url=f"{MAIN_URL}{API_LOGIN}")
        
        token_data = await validate_token(token_key)
        request.state.user = token_data

        response = await call_next(request)
        return response