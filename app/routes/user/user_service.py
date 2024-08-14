from fastapi import Request
from fastapi.responses import JSONResponse

import json

from models.user_dto import UserModel
from db.context import user_collection
from datetime import datetime
from bson import ObjectId
from models.user_dto import *
from routes._modules import list_module
from models import user_dto



async def create_user(item: UserModel):
    insert_user_by_item = user_collection.insert_one(item.model_dump())

    return str(insert_user_by_item.inserted_id)

async def get_user_list(request: Request) -> JSONResponse:
    match = {}
    projection = {"_id": 1, "company_nm": 1, "user_nm": 1, "email": 1, "created_at": 1, "del_yn": 1}
    
    user_list = await list_module.get_collection_list(
        match,
        user_collection,
        projection,
        ResponseUserListModel,
        user_dto
        )
    
    content = {
        "total": len(user_list),
        "list": user_list
    }
    response_content=json.loads(json.dumps(content, indent=1, default=str))
    
    return response_content

async def get_user_detail(request: Request) -> JSONResponse:
    user_id = request.query_params.get("_id")
    match = {"_id": ObjectId(user_id)}
    projection = {"company_field": 0}
    
    user_list = await list_module.get_collection_list(
        match,
        user_collection,
        projection,
        ResponseUserListModel,
        user_dto
        )

    response_content=json.loads(json.dumps(user_list, indent=1, default=str))
    
    return response_content
# def get(limit: int, offset: int) -> list[db.User]:
#     return user_db.get(limit=limit, offset=offset)
            
# def get_by_id(id: int) -> db.User | None:
#     return user_db.get_by_id(id)
    
# def get_by_email(email: str) -> db.User | None:
#     return user_db.get_by_email(email.lower().strip())

# def create(name: str, surname: str, role: db.User.Role, email: str, password: str) -> db.User:
#     name = formating.format_string(name)
#     surname = formating.format_string(surname)
#     email = formating.format_string(email)
#     return user_db.add(name, surname, role, email)

# def update(id: int, name: str, surname: str, role: db.User.Role, email: str, password: str) -> None:
#     name = formating.format_string(name)
#     surname = formating.format_string(surname)
#     email = formating.format_string(email)
#     user_db.update(id ,name, surname, role, email)
    
# def update_name_surname(id: int, name: str, surname: str) -> None:
#     user = get_by_id(id)
#     if user is None:
#         return
    
#     name = formating.format_string(name)
#     surname = formating.format_string(surname)
#     user_db.update(
#         user.id,
#         name,
#         surname,
#         user.role,
#         user.email,
#         user.password
#     )

# def update_password(id: int, new_password: str) -> None:
#     user = get_by_id(id)
#     if user is None:
#         return
    
#     user_db.update(
#         user.id,
#         user.name,
#         user.surname,
#         user.role,
#         user.email,
#     )

# def reset_password(id: int) -> str:    
#     user = get_by_id(id)
#     if user is None:
#         return
    
#     new_password = str(randint(100000, 999999))
#     user_db.update(
#         user.id,
#         user.name,
#         user.surname,
#         user.role,
#         user.email,
#     )
    
#     return new_password
    
# def delete(id: int) -> None:
#     user_db.delete(id)
    
    