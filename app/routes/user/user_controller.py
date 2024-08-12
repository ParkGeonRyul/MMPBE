from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi import HTTPException

from routes.user import user_service
from utils import dependencies
from models.user_dto import UserModel
from routes.user import user_service
from routes._path.api_paths import CREATE_USER, READ_USER
# -------------------------------------------------

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from constants import COOKIES_KEY_NAME

import os
import msal

from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from dotenv import load_dotenv
from db.context import auth_collection, user_collection
from utils.objectId_convert import objectId_convert
from fastapi import Request, HTTPException, status

load_dotenv()
router = APIRouter()


@router.post(CREATE_USER)
async def create_user(item: UserModel):
    return await user_service.create_user(item)

@router.get(READ_USER)
async def get_user(request: Request):
    return await user_service.get_user(request)
# @router.get("/all", response_model=list[dto.GetUser])
# def get_all(limit: int = Query(1000, gt=0), offset: int = Query(0, ge=0)) -> list[db.User]:
#     return user_service.get(limit, offset)

# @router.get("/{id}", response_model=dto.GetUser)
# def get_by_id(id: int = Path(ge=1)) -> db.User | None:
#     user = user_service.get_by_id(id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user

# @router.get("/email/{email}", response_model=dto.GetUser)
# def get_by_email(email: str) -> db.User | None:
#     user = user_service.get_by_email(email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user    