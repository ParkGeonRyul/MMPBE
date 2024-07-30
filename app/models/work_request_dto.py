from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class WorkRequestField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="고객 ID(ObjectID)",
        alias="userId"
    )
    request_plan_id = Field(
        description="작업계획서(ObjectID)",
        min_length=1,
        default=None,
        alias="requestPlanId"
    )
    contact_nm = Field(
        description="담당자 이름(Maven)",
        example="Aiden",
        default=None,
        alias="contactNm"
    )
    request_title = Field(
        description="요청 제목",
        example="Web DNS 설정",
        min_length=1,
        alias="requestTitle"
    )
    customer_nm = Field(
        description="고객명",
        example="고영희",
        min_length=1,
        alias="customerNm"
    )
    request_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=None,
        alias="requestDate"
    )
    content = Field(
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
        default=None,
        alias="acceptorNm"
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

class CreateWorkRequestModel(BaseModel): # fe -> be
    user_id: str = WorkRequestField.user_id # id 
    request_plan_id: str = WorkRequestField.request_plan_id # 작업계획서가 생성 될 때 update
    contact_nm: str = WorkRequestField.contact_nm # 담당자 이름 (필수) 추후 ID로
    request_title: str = WorkRequestField.request_title # 필수
    request_date: Optional[datetime] = WorkRequestField.request_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    content: str = WorkRequestField.content
    file: Optional[str] = WorkRequestField.file
    status: Optional[str] = WorkRequestField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
    created_at: Optional[datetime] = WorkRequestField.created_at # 최초 이후 수정이 안 됨
    updated_at: Optional[datetime] = WorkRequestField.updated_at 
    del_yn: Optional[str] = WorkRequestField.del_yn # 시스템 관리자를 위한
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "requestPlanId": "작업계획서(ObjectID)",
                "contactNm": "담당자 이름(Maven)",
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "delYn": "삭제 여부"
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
                "userId": "6690cf7fa4897bf6b90541c1",
                "requestPlanId": "작업계획서(ObjectID)",
                "contactNm": "담당자 이름(Maven)",
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "delYn": "삭제 여부"
            }
        }
    )

class DeleteRequestTempraryModel(BaseModel):
    ids: List[str]

class UpdateDelYnWorkRequestModel(BaseModel):
    request_id: str = Field(description="작업 요청 ID", alias="requestId")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "request_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
            }
        }
    )