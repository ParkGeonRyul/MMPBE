from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse
from httpx import AsyncClient

from utils import formating
from services import user_service
from utils import dependencies
from constants import COOKIES_KEY_NAME, SESSION_TIME

import os
from dotenv import load_dotenv
import msal


load_dotenv()
router = APIRouter()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")
MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"
MS_AUTHORITY = "https://login.microsoftonline.com/common"
PARTNER_CENTER_URL = os.getenv("PARTNER_CENTER_URL")

msal_app = msal.ConfidentialClientApplication(
    MS_CLIENT_ID,
    authority=MS_AUTHORITY,
    client_credential=MS_CLIENT_SECRET
)

@router.get("/login")
def login_on_ms():
    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
        redirect_uri=MS_REDIRECT_URI
    )
    return RedirectResponse(auth_url)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read", "https://accountmgmtservice.dce.mp.microsoft.com/user_impersonation"],
        redirect_uri=MS_REDIRECT_URI
    )

    if "access_token" not in result:
        raise HTTPException(status_code=400, detail=result.get("error_description"))

    access_token = result["access_token"]

    async with AsyncClient() as client:
        user_response = await client.get(
            MS_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=user_response.status_code, detail=user_response.text)

        user_data = user_response.json()
        partner_response = await client.get(
            PARTNER_CENTER_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if partner_response.status_code != 200:
            raise HTTPException(status_code=partner_response.status_code, detail=partner_response.text)

        partner_data = partner_response.json()

    return JSONResponse(content={"user_data": user_data, "partner_data": partner_data})


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
    return 