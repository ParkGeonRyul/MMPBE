from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class UsersFields:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    company_id = Field(
        description="회사 ID(ObjectID)",
        default=None
    )
    user_nm = Field(
        description="사용자 이름",
        min_length=2,
        max_length=20
    )
    rank = Field(
        description="직급",
        examples="프로"
    )
    company_contact=Field(
        description="고객사 연락처",
        examples="02)000-0000",
        default=None
    )
    mobile_contact = Field(
        description="고객사 mobile",
        examples="010-0000-0000"
    )
    email = Field(
        description="사용자 이메일",
        examples="maven.kim@mavencloudservice.com",
        pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    )
    responsible_party = Field(
        description="분류",
        examples="엔지니어",
        default=None
    )
    role = Field(
        description = "역할 ID(INDEX)",
        examples="0 = client, 1 = admin, 2 = Super admin",
        ge=0,
        le=2
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
        default="N"
    )

class UserModel(BaseModel):
    id: Optional[PyObjectId] = UsersFields.id
    company_id: Optional[str] = UsersFields.company_id
    user_nm : str = UsersFields.user_nm
    rank: str = UsersFields.rank
    company_contact: Optional[str] = UsersFields.company_contact
    mobile_contact: str = UsersFields.mobile_contact
    email: str = UsersFields.email
    responsible_party: str = UsersFields.responsible_party
    role: int = UsersFields.role
    created_at: Optional[datetime] = UsersFields.created_at
    updated_at: Optional[datetime] = UsersFields.updated_at
    del_yn: Optional[str] = UsersFields.del_yn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "company_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "user_nm": "고객 이름",
                "rank": "직급",
                "company_contact": "고객사 연락처",
                "mobile_contact": "고객사 mobile",
                "email": "고객사 Email",
                "responsible_party": "고객 분류",
                "role": "역할(Integer)"
            }
        }
    )

class UserCollection(BaseModel):
    users: List[UserModel]
    

