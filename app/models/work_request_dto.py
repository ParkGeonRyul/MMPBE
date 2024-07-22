from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class workRequestField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    userId = Field(
        description="고객 ID(ObjectID)"
    )
    deviceNm = Field(
        description="장비 이름",
        example="Server-1",
        min_length=1
    )
    contactNm = Field(
        description="담당자 이름(Maven)",
        example="Aiden",
        min_length=1
    )
    requestTitle = Field(
        description="요청 제목",
        example="Web DNS 설정",
        min_length=1
    )
    customerNm = Field(
        description="고객명",
        example="고영희",
        min_length=1
    )
    requestDt = Field(
        description="요청 일자(UTC + 0)"
    )
    workContent = Field(
        description="작업 내용",
        min_length=1
    )
    file = Field(
        description="첨부 파일",
        example="Zone파일.zip",
        min_length=1
    )
    status = Field(
        description="승인 여부",
        example="보류, 승인, 거절",
        default=None
    )
    acceptorNm = Field(
        description="승인자 이름",
        example="Aiden"
    )
    regYn = Field(
        description="작업 요청 상태",
        examples="Y(요청), N(회수)",
        default="Y"
    )
    createdAt = Field(
        description="생성 날짜(UTC + 0)",
        default=None
    )
    updatedAt = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=datetime.now()
    )
    delYn = Field(
        description="삭제된 여부",
        default="N"
    )

class workRequestModel(BaseModel):
    id: Optional[PyObjectId] = workRequestField.id
    userId: str = workRequestField.userId
    deviceNm: str = workRequestField.deviceNm
    contactNm: str = workRequestField.contactNm
    requestTitle: str = workRequestField.requestTitle
    customerNm: str = workRequestField.customerNm
    requestDt: datetime = workRequestField.requestDt
    workContent: str = workRequestField.workContent
    file: str = workRequestField.file
    status: str = workRequestField.status
    acceptorNm: str = workRequestField.acceptorNm
    regYn: str = workRequestField.regYn
    createdAt: Optional[datetime] = workRequestField.createdAt
    updatedAt: Optional[datetime] = workRequestField.updatedAt
    delYn: Optional[str] = workRequestField.delYn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "diviceNm": "장비 이름",
                "contactNm": "담당자 이름(Maven)",
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDt": "요청 일자 (UTC + 0)",
                "workContent": "작업 내용",
                "file": "파일 명",
                "status": "승인 여부",
                "acceptorNm": "승인자 이름",
                "regYn": "작업 요청"
            }
        }
    )

class  updateWorkRequestModel(BaseModel):
    id: Optional[PyObjectId] = None
    userId: Optional[str] = None
    deviceNm: Optional[str] = None
    contactNm: Optional[str] = None
    requestTitle: Optional[str] = None
    customerNm: Optional[str] = None
    requestDt: Optional[datetime] = None
    workContent: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = None
    acceptorNm: Optional[str] = None
    regYn: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    delYn: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "diviceNm": "장비 이름",
                "contactNm": "담당자 이름(Maven)",
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDt": "요청 일자 (UTC + 0)",
                "workContent": "작업 내용",
                "file": "파일 명",
                "status": "승인 여부",
                "acceptorNm": "승인자 이름",
                "regYn": "작업 요청"
            }
        }
    )

class workRequestCollection(BaseModel):
    workRequests: List[workRequestModel]