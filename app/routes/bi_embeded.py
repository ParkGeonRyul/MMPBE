from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv

import json
import requests
import msal

from constants import COOKIES_KEY_NAME
from routes._path.main_path import MAIN_URL, API_URL
from routes._modules.jwt import *
from routes._path.api_paths import *
from routes._path.ms_paths import *
from routes.auth.auth_service import *
from db.context import auth_collection
from models.work_request_dto import *


load_dotenv()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")

router = APIRouter()

class Router:
    def __init__(self):
        pass

@router.get("/bi-embeded", status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def get_request_list(request: Request) -> JSONResponse:
    groupId = request.query_params.get("groupId")
    reportId = request.query_params.get("reportId")
    token_key = await parse_token(request.cookies.get(COOKIES_KEY_NAME))

    auth_data = auth_collection.find_one({"_id": ObjectId(token_key)})
    refresh_token = auth_data['refresh_token']

    async with AsyncClient() as client:
        bi_token_response = await client.post(
            MS_TOKEN_URL,
            data={
                "client_id": MS_CLIENT_ID,
                'scope': 'https://analysis.windows.net/powerbi/api/.default',
                "client_secret": MS_CLIENT_SECRET,
                "redirect_uri": MS_REDIRECT_URI,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    bi_data = bi_token_response.json()

    headers = {
        'Authorization': f'Bearer {bi_data['access_token']}'
    }

    data = {
        "accessLevel": "view"
    }

    get_token = requests.post(f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}/GenerateToken", headers=headers, data=data)
    token_json = get_token.json()

    return JSONResponse(content=token_json['token'])


@router.get("/tested", status_code=status.HTTP_200_OK, response_model_by_alias=True)
async def get_request_list(request: Request) -> JSONResponse:
    groupId = request.query_params.get("groupId")
    reportId = request.query_params.get("reportId")
    token_key = await parse_token(request.cookies.get(COOKIES_KEY_NAME))

    auth_data = auth_collection.find_one({"_id": ObjectId(token_key)})
    refresh_token = auth_data['refresh_token']

    async with AsyncClient() as client:
        gra_token_response = await client.post(
            MS_TOKEN_URL,
            data={
                "client_id": MS_CLIENT_ID,
                "client_secret": MS_CLIENT_SECRET,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "scope": 'https://monitoring.azure.com/.default'
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        token_json = gra_token_response.json()

    return token_json