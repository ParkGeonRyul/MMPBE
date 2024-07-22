from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class maintenanceField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    userId = Field(
        description="고객 ID(ObjectID)"
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
    contractDt = Field(
        description="계약 날짜(UTC + 0)"
    )
    approvalYn = Field(
        description="승인 여부",
        example="Y, N",
        default=None
    )
    status = Field(
        description="작업 상태 확인",
        example="OO 작업 중",
        default=None
    )
    createdAt = Field(
        description="생성 날짜(UTC + 0), 임시저장 상태일 때는 NULL",
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

class maintenanceModel(BaseModel):
    id: Optional[PyObjectId] = maintenanceField.id
    userId: str = maintenanceField.userId
    title: str = maintenanceField.title
    content: str = maintenanceField.content
    file: Optional[str] = maintenanceField.file
    contractDt: datetime = maintenanceField.contractDt
    approvalYn: Optional[str] = maintenanceField.approvalYn
    status: Optional[str] = maintenanceField.status
    createdAt: Optional[datetime] = maintenanceField.createdAt
    updatedAt: Optional[datetime] = maintenanceField.updatedAt
    delYn: Optional[str] = maintenanceField.delYn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "title": "제목",
                "content": "내용",
                "file": "파일 경로",
                "contractDt": "계약 날짜"
            }
        }
    )

class updateMaintenanceModel(BaseModel):
    id: Optional[PyObjectId] = None
    userId: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    file: Optional[str] = None
    contractDt: Optional[datetime] = None
    approvalYn: Optional[str] = None
    status: Optional[str] = None
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
                "title": "제목",
                "content": "내용",
                "file": "파일 경로",
                "contractDt": "계약 날짜"
            }
        }
    )

class maintenanceCollection(BaseModel):
    maintenances: List[maintenanceModel]