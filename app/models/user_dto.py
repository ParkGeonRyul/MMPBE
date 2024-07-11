from datetime import datetime

from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List
from typing_extensions import Annotated


class UsersFields:
    companyId = Field(
        description="회사 ID(ObjectID)"
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
        description="회사 전화번호",
        examples="02)000-0000"
    )
    mobileContact = Field(
        description="모바일 전화번호",
        examples="010-0000-0000"
    )
    email = Field(
        description="사용자 이메일",
        examples="maven.kim@mavencloudservice.com",
        pattern=r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    )
    responsibleParty = Field(
        description="분류",
        examples="엔지니어"
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

class UserDTO(BaseModel):
    _id: str
    companyId: str = UsersFields.companyId
    userNm : str = UsersFields.userNm
    rank: str = UsersFields.rank
    companyContact: str = UsersFields.companyContact
    mobileContact: str = UsersFields.mobileContact
    email: str = UsersFields.email
    responsibleParty: str = UsersFields.responsibleParty
    role: int = UsersFields.role
    createdAt: datetime = UsersFields.createdAt
    updatedAt: datetime = UsersFields.updatedAt
    delYn: str = UsersFields.delYn

