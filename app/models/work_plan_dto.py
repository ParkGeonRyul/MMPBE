from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class WorkPlanField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="작업계획서 수신자 id(ObjectID)",
        alias="requester_id"
    )
    acceptor_id = Field(
        description="작업계획서 발신자 id(ObjectID)",
        min_length=1,
        default=None,
        alias="planId"
    )
    request_id = Field(
        description="작업 요청서 id(ObjectID)",
        min_length=1,
        default=None,
        alias="requestId"
    )
    plan_title = Field(
        description="계획서 제목",
        example="Web DNS 설정",
        min_length=1,
        alias="planTitle"
    )
    plan_content = Field(
        description="계획서 내용",
        min_length=1,
        alias= "planContent"
    )
    plan_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=None,
        alias="planDate"
    )
    file = Field(
        description="첨부 파일",
        example="Zone파일.zip",
        default=None,
        alias="file"
    )
    status = Field(
        description="승인 여부",
        example="요청, 회수, 승인, 반려",
        default=None,
        alias="status"
    )
    status_content = Field(
        description="승인/반려 내용",
        example="승인내용, 반려사유",
        default=None,
        alias="statusContent"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now(),
        alias="createdAt"
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None,
        alias="updatedAt"
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N",
        alias="delYn"
    )

class CreateWorkPlanModel(BaseModel): # fe -> be
    user_id: str = WorkPlanField.user_id #등록자 id (작업계획서 수신자 id)
    acceptor_id: str = WorkPlanField.acceptor_id # 발신자 id (작업요청자 수신자 id)
    request_id: str = WorkPlanField.request_id # 작업 요청서 id
    plan_title: str = WorkPlanField.plan_title # 필수
    plan_content: str = WorkPlanField.plan_content
    plan_date: Optional[datetime] = WorkPlanField.plan_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    file: Optional[str] = WorkPlanField.file #파일경로
    status: Optional[str] = WorkPlanField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
    status_content : Optional[str] = WorkPlanField.status_content # 승인내용, 반려사유 (계획서 수신자가 작성)
    created_at: Optional[datetime] = WorkPlanField.created_at # 최초 이후 수정이 안 됨
    updated_at: Optional[datetime] = WorkPlanField.updated_at 
    del_yn: Optional[str] = WorkPlanField.del_yn # 시스템 관리자를 위한
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "acceptorId": "작업요청자 수신자 id(ObjectID)",
                "requestId": "작업계획서(ObjectID)",
                "planTitle": "계획서 제목",
                "planContent": "계획서 내용",
                "planDate": "2024-08-05 00:00:00",
                "file": "파일 명",
                "status": "요청",
                "acceptorNm" : "제갈길동" ,
                "createdAt" : "2024-08-05 00:00:00",
                "updatedAt" : "2024-08-05 00:00:00",                
                "delYn": "N"
            }
        }
    )

class  UpdateWorkPlanModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    device_nm: Optional[str] = None
    contact_nm: Optional[str] = None
    plan_title: Optional[str] = None
    customer_nm: Optional[str] = None
    plan_dt: Optional[datetime] = None
    plan_content: Optional[str] = None
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
                "status": "승인",
                "delYn": "삭제 여부"
            }
        }
    )

class  UpdatePlanStatusAcceptModel(BaseModel):
    id: Optional[PyObjectId] = None
    status: Optional[str] = None
    statusContent: Optional[str] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "status": "승인",
                "statusContent": "승인내용",
                "updated_at": "new Date() 오늘날짜"
            }
        }
    )

class DeletePlanTempraryModel(BaseModel):
    ids: List[str]

class UpdateDelYnWorkPlanModel(BaseModel):
    plan_id: str = Field(description="작업 요청 ID", alias="requestId")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "plan_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
            }
        }
    )