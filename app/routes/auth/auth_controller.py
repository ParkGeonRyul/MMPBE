from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse

from constants import COOKIES_KEY_NAME
from routes.auth import auth_service
from routes._path.api_paths import AUTH_CALLBACK, CHECK_SESSION, LOGIN_WITH_MS, LOGOUT, USER_INFO


router = APIRouter()

@router.get("/test_mid")
async def test(request: Request):
    test = request.state.user
    print(type(test))
    return None

@router.get(LOGIN_WITH_MS)
async def login():
    redirect_callback = await auth_service.login()

    return redirect_callback

@router.get(AUTH_CALLBACK)
async def auth_callback(request: Request) -> RedirectResponse:
    auth_code = request.query_params.get("code")
    redirect = await auth_service.auth_callback(auth_code)

    return redirect

@router.get(LOGOUT, status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)

@router.get(CHECK_SESSION)
async def validate(request: Request) -> JSONResponse:
    return await auth_service.validate(request)

@router.get(USER_INFO,
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },response_class=Response)
async def get_user_profile_image(request: Request) -> JSONResponse:
    return await auth_service.get_user_profile_image(request)