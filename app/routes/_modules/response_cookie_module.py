import json
import pymongo

from db.context import auth_collection
from fastapi.responses import JSONResponse
from constants import COOKIES_KEY_NAME

async def set_response_cookie(token_data: dict, content: json):
        response = JSONResponse(content=content)
        if token_data['status'] == "refresh":
            access_token = auth_collection.find_one({"user_id": token_data['userId']})['access_token']
            response.set_cookie(key=COOKIES_KEY_NAME, value=access_token, httponly=True)
            
        return response