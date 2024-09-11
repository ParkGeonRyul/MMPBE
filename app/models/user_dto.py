from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

import re

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId
from pydantic.alias_generators import to_camel
from utils.snake_by_camel import *


class UsersFields:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    company_id = Field(
        description="회사 ID(ObjectID)",
        default="66a98cab9adf7a6e2805e6d3",
        alias="companyId"
    )
    user_nm = Field(
        description="사용자 이름",
        min_length=2,
        alias="userNm"
    )
    rank = Field(
        description="직급",
        example="프로",
        default="프로"
    )
    company_contact=Field(
        description="고객사 연락처",
        example="02)000-0000",
        default=None,
        alias="companyContact"
    )
    mobile_contact = Field(
        description="고객사 mobile",
        example="010-0000-0000",
        alias="mobileContact",
        default=None
    )
    email = Field(
        description="사용자 이메일",
        example="maven.kim@mavencloudservice.com",
        pattern=r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
    )
    responsible_party = Field(
        description="분류",
        example="엔지니어",
        default=None,
        alias="responsibleParty"
    )
    role = Field(
        description = "역할 ID(INDEX)",
        example="client, admin, system admin",
        default="66a83425be3a5f7919351fc1"
    )
    created_at = Field(
        description="오늘 날짜(UTC + 0)",
        default=datetime.now()
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N",
        alias="delYn"
    )

class UserModel(BaseModel):
    company_id: Optional[str] = UsersFields.company_id
    user_nm : str = UsersFields.user_nm
    rank: Optional[str] = UsersFields.rank
    company_contact: Optional[str] = UsersFields.company_contact
    mobile_contact: Optional[str] = UsersFields.mobile_contact
    email: str = UsersFields.email
    responsible_party: Optional[str] = UsersFields.responsible_party
    role: Optional[str] = UsersFields.role
    created_at: Optional[datetime] = UsersFields.created_at
    updated_at: Optional[datetime] = UsersFields.updated_at
    del_yn: Optional[str] = UsersFields.del_yn
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "회사ID(ObjectId)",
                "userNm": "고객 이름",
                "rank": "직급",
                "companyContact": "고객사 연락처",
                "mobileContact": "고객사 mobile",
                "email": "고객사 Email",
                "responsibleParty": "고객 분류",
                "role": "역할(User, Admin, SystemAdmin)"
            }
        }
    )

class UserCollection(BaseModel):
    users: List[UserModel]

class ResponseUserListModel(BaseModel):
    id: str = Field(alias="_id")
    company_nm: Optional[str] = Field(alias="companyNm")
    user_nm : str = Field(alias="userNm")
    email: str
    created_at: Optional[datetime] = Field(alias="createdAt")
    mobile_contact: Optional[str] = Field(alias="mobileContact")
    del_yn: Optional[str] = Field(alias="delYn")
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        alias_generator=to_camel,
        json_schema_extra={
            "example": {
                "_id": "ObjectID",
                "companyNm": "고객사 이름",
                "userNm": "고객 이름",
                "email": "고객사 Email",
                "createdAt": "생성 날짜",
                "delYn": "삭제 여부"
            }
        }
    )

class ResponseUserDtlModel(BaseModel):
    id: str = Field(alias="_id")
    company_id: Optional[str] = Field(alias="companyId")
    company_nm: Optional[str] = Field(alias="companyNm")
    user_nm : str = Field(alias="userNm")
    rank: str
    company_contact: Optional[str] = Field(alias="companyContact")
    mobile_contact: str = Field(alias="mobileContact")
    email: str
    responsible_party: Optional[str] = Field(alias="responsibleParty")
    role: Optional[str]
    created_at: Optional[datetime] = Field(alias="createdAt")
    del_yn: Optional[str] = Field(alias="delYn")
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        alias_generator=to_camel,
        json_schema_extra={
            "example": {
                "_id": "ObjectID",
                "companyId": "회사ID(ObjectId)",
                "userNm": "고객 이름",
                "rank": "직급",
                "companyContact": "고객사 연락처",
                "mobileContact": "고객사 mobile",
                "email": "고객사 Email",
                "responsibleParty": "고객 분류",
                "role": "역할(User, Admin, SystemAdmin)",
                "createdAt": "생성 날짜",
                "delYn": "삭제 여부"
            }
        }
    )
    
async def get_list(match: dict, projection: dict, db_collection: any, response_model: any):
    pipeline = [
        {
            "$match": match
        },
        {
            "$lookup": {
                "from": "company",
                "let": { "companyId": "$company_id" },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": [ {"$toString": "$_id"}, "$$companyId"]
                            }
                        }
                    }
                ],
                "as": "company_field"
                }
        },
        {
            "$unwind": "$company_field"
        },
        {
            "$set": {
                "company_nm": "$company_field.company_nm"
            }
        },
        {
            "$project": projection
        }
    ]
    results = db_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        item['created_at'] = str(item['created_at'])
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content

async def get_dtl(match: dict, projection: dict, db_collection: any, response_model: any):
    pipeline = [
        {
            "$match": match
        },
        {
            "$lookup": {
                "from": "company",
                "let": { "companyId": "$company_id" },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": [ {"$toString": "$_id"}, "$$companyId"]
                            }
                        }
                    }
                ],
                "as": "company_field"
                }
        },
        {
            "$unwind": "$company_field"
        },
        {
            "$set": {
                "company_nm": "$company_field.company_nm"
            }
        },
        {
            "$project": projection
        }
    ]
    results = db_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        item['created_at'] = str(item['created_at'])
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
    convert_content = convert_keys_to_camel_case(content)

    return convert_content[0]

