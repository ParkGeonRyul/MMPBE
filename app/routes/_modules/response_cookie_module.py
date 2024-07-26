import json
import pymongo

from db.context import work_request_collection, auth_collection, user_collection
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from db.context import Database
from routes.auth import auth_service
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner
from models.work_request_dto import WorkRequestModel, UpdateWorkRequestModel
from constants import COOKIES_KEY_NAME
from utils.objectId_convert import objectId_convert
from routes._modules import list_module
from routes._modules.list_module import NotNull

def set_response_cookie(token_data: dict, content: any, access_token: str):
        
        response = JSONResponse(content=content)
        response.set_cookie(key=COOKIES_KEY_NAME, value=access_token, httponly=True)

        return response