from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class MaintenanceField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="고객 ID(ObjectID)",
        alias="userId"
    )
    title = Field(
        description="계약 자료 제목",
        min_length=1
    )
    content = Field(
        description="계약 내용",
        min_length=1
    )
    file = Field(
        description="계약 자료 관련 파일",
        examples="jun.zip",
        min_length=1
    )
    contract_date = Field(
        description="계약 날짜(UTC + 0)",
        alias="contractDate"
    )
    approval_yn = Field(
        description="승인 여부",
        example="Y, N",
        default=None,
        alias="approvalYn"
    )
    status = Field(
        description="작업 상태 확인",
        example="OO 작업 중",
        default=None
    )
    created_at = Field(
        description="생성 날짜(UTC + 0), 임시저장 상태일 때는 NULL",
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

class CreateMaintenanceModel(BaseModel):
    user_id: str = MaintenanceField.user_id
    title: str = MaintenanceField.title
    content: str = MaintenanceField.content
    file: Optional[str] = MaintenanceField.file
    contract_date: datetime = MaintenanceField.contract_date
    approval_yn: Optional[str] = MaintenanceField.approval_yn
    status: Optional[str] = MaintenanceField.status
    created_at: Optional[datetime] = MaintenanceField.created_at
    updated_at: Optional[datetime] = MaintenanceField.updated_at
    del_yn: Optional[str] = MaintenanceField.del_yn
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "고객사ID(ObjectId)",
                "title": "제목",
                "content": "내용",
                "file": "파일 경로",
                "contract_date": "계약 날짜"
            }
        }
    )

class UpdateMaintenanceModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    file: Optional[str] = None
    contract_date: Optional[datetime] = None
    approval_yn: Optional[str] = None
    status: Optional[str] = None
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
                "title": "제목",
                "content": "내용",
                "file": "파일 경로",
                "contract_date": "계약 날짜"
            }
        }
    )

class MaintenanceCollection(BaseModel):
    maintenances: List[CreateMaintenanceModel]