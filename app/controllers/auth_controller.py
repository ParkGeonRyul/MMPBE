from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating
from models import db
from models import dto
from services import user_service
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@router.post("/login", status_code=status.HTTP_200_OK, response_model=str)
async def login( res: Response):
# async def login(dto: dto.LoginUser, res: Response):
    # NOW = datetime.now(timezone.utc)
    
    # email = formating.format_string(dto.email)
    
    # user = user_service.get_by_email(email)
    # if user is None:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    # if HashLib.validate(dto.password, user.password) is False:
    #     raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
    
    # exp_date = NOW + SESSION_TIME
    # token = jwt_service.encode(user.id, user.role, exp_date)
    # res.set_cookie(COOKIES_KEY_NAME, token, expires=exp_date)
    # return token
    return ;

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
    return ;