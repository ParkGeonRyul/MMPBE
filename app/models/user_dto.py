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
    companyId = Field(
        description="회사 ID(ObjectID)",
        default=None
    )
    userNm = Field(
        description="사용자 이름",
        min_length=2,
        max_length=20
    )
    rank = Field(
        description="직급",
        examples="프로"
    )
    companyContact=Field(
        description="고객사 연락처",
        examples="02)000-0000",
        default=None
    )
    mobileContact = Field(
        description="고객사 mobile",
        examples="010-0000-0000"
    )
    email = Field(
        description="사용자 이메일",
        examples="maven.kim@mavencloudservice.com",
        pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    )
    responsibleParty = Field(
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
    createdAt = Field(
        description="오늘 날짜(UTC + 0)",
        default=datetime.now()
    )
    updatedAt = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    delYn = Field(
        description="삭제된 여부",
        default="N"
    )

class UserModel(BaseModel):
    id: Optional[PyObjectId] = UsersFields.id
    companyId: Optional[str] = UsersFields.companyId
    userNm : str = UsersFields.userNm
    rank: str = UsersFields.rank
    companyContact: Optional[str] = UsersFields.companyContact
    mobileContact: str = UsersFields.mobileContact
    email: str = UsersFields.email
    responsibleParty: str = UsersFields.responsibleParty
    role: int = UsersFields.role
    createdAt: Optional[datetime] = UsersFields.createdAt
    updatedAt: Optional[datetime] = UsersFields.updatedAt
    delYn: Optional[str] = UsersFields.delYn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "userNm": "고객 이름",
                "rank": "직급",
                "companyContact": "고객사 연락처",
                "mobileContact": "고객사 mobile",
                "email": "고객사 Email",
                "responsibleParty": "고객 분류",
                "role": "역할(Integer)"
            }
        }
    )

class UserCollection(BaseModel):
    users: List[UserModel]
    

