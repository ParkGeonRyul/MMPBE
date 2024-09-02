from fastapi import APIRouter, status
from fastapi.requests import Request

from models.work_request_dto import *
from routes._path.api_paths import CATEGORY
from routes.category import category_service


router = APIRouter()

class Router:
    def __init__(self):
        pass

@router.get(CATEGORY, status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def get_category(request: Request):
       
       return await category_service.get_category(request)

