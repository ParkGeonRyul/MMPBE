from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class WorkRequestField:
    # id = Field(
    #     description="ObjectID",
    #     alias="_id",
    #     default_factory=PyObjectId
    # )
    user_id = Field(
        description="고객 ID(ObjectID)"
    )
    device_nm = Field(
        description="장비 이름",
        example="Server-1",
        min_length=1
    )
    contact_nm = Field(
        description="담당자 이름(Maven)",
        example="Aiden",
        default=None
    )
    request_title = Field(
        description="요청 제목",
        example="Web DNS 설정",
        min_length=1
    )
    customer_nm = Field(
        description="고객명",
        example="고영희",
        min_length=1
    )
    request_dt = Field(
        description="요청 일자(UTC + 0)"
    )
    work_content = Field(
        description="작업 내용",
        min_length=1
    )
    file = Field(
        description="첨부 파일",
        example="Zone파일.zip",
        default=None
    )
    status = Field(
        description="승인 여부",
        example="보류, 승인, 거절",
        default=None
    )
    acceptor_nm = Field(
        description="승인자 이름",
        example="Aiden",
        default=None
    )
    reg_yn = Field(
        description="작업 요청 상태",
        example="Y, N",
        default="Y"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0)",
        default=None
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=datetime.now()
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N"
    )

class WorkRequestModel(BaseModel):
    user_id: str = WorkRequestField.user_id
    device_nm: str = WorkRequestField.device_nm
    contact_nm: Optional[str] = WorkRequestField.contact_nm
    request_title: str = WorkRequestField.request_title
    customer_nm: str = WorkRequestField.customer_nm
    request_dt: datetime = WorkRequestField.request_dt
    work_content: str = WorkRequestField.work_content
    file: Optional[str] = WorkRequestField.file
    status: Optional[str] = WorkRequestField.status
    acceptor_nm: Optional[str] = WorkRequestField.acceptor_nm
    reg_yn: Optional[str] = WorkRequestField.reg_yn
    created_at: Optional[datetime] = WorkRequestField.created_at
    updated_at: Optional[datetime] = WorkRequestField.updated_at
    del_yn: Optional[str] = WorkRequestField.del_yn
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "user_id": "6690cf7fa4897bf6b90541c1",
                "diviceNm": "장비 이름",
                "contact_nm": "담당자 이름(Maven)",
                "request_title": "요청 제목",
                "customer_nm": "고객 이름",
                "request_dt": "2024-07-19 08:06:05.064246",
                "work_content": "작업 내용",
                "file": "파일 명",
                "status": "승인 여부",
                "acceptor_nm": "승인자 이름",
                "reg_yn": "작업 요청"
            }
        }
    )

class  UpdateWorkRequestModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    device_nm: Optional[str] = None
    contact_nm: Optional[str] = None
    request_title: Optional[str] = None
    customer_nm: Optional[str] = None
    request_dt: Optional[datetime] = None
    work_content: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = None
    acceptor_nm: Optional[str] = None
    reg_yn: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    del_yn: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "device_nm": "장비 이름",
                "contact_nm": "담당자 이름(Maven)",
                "request_title": "요청 제목",
                "customer_nm": "고객 이름",
                "request_dt": "요청 일자 (UTC + 0)",
                "work_content": "작업 내용",
                "file": "파일 명",
                "status": "승인 여부",
                "acceptor_nm": "승인자 이름",
                "reg_yn": "작업 요청"
            }
        }
    )

class UpdateDelYnWorkRequestModel(BaseModel):
    id: str