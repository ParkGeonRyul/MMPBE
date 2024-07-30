from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class ContractDataField:
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
        min_length=1,
        default=None
    )
    contract_date = Field(
        description="계약 날짜(UTC + 0)",
        default=None,
        alias="contractDate"
    )
    approval_yn = Field(
        description="승인 여부",
        example="Y, N",
        default=None,
        alias="approvalYn"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0), 임시저장 상태일 때는 NULL 처리",
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

class ContractDataModel(BaseModel):
    id: Optional[PyObjectId] = ContractDataField.id
    user_id: str = ContractDataField.user_id
    title: str = ContractDataField.title
    content: str = ContractDataField.content
    file: Optional[str] = ContractDataField.file
    contract_date: datetime = ContractDataField.contract_date
    approval_yn: Optional[str] = ContractDataField.approval_yn
    created_at: Optional[datetime] = ContractDataField.created_at
    updated_at: datetime = ContractDataField.updated_at
    del_yn: Optional[str] = ContractDataField.del_yn
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "ObjectId",
                "title": "제목",
                "content": "내용",
                "file": "파일 경로명 or NULL",
                "contract_date": "임시저장일때는 NULL, UTC + 0",
                "updated_at": "UTC + 0"
            }
        }
    )

class UpdateContractDataModel(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    file: Optional[str] = None
    contract_date: Optional[datetime] = None
    approval_yn: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    del_yn: Optional[str] = None
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "title": "제목",
                "content": "내용",
                "file": "파일 경로명",
                "contract_date": "UTC + 0",
                "approval_yn": "Y or N or """,
                "created_at": "UTC + 0",
                "updated_at": "UTC + 0",
                "del_yn": "Y or N or """
            }
        }
    )

class ContractDataCollection(BaseModel):
    contract_datas: List[ContractDataModel]