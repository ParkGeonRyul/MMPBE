from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class MaintenanceField:
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

class ContractDataDTO(BaseModel):
    _id: str
    userId: str = MaintenanceField.userId
    title: str = MaintenanceField.title
    content: str = MaintenanceField.content
    file: str = MaintenanceField.file
    contractDt: datetime = MaintenanceField.contractDt
    approvalYn: str = MaintenanceField.approvalYn
    status: str = MaintenanceField.status
    createdAt: datetime = MaintenanceField.createdAt
    updatedAt: datetime = MaintenanceField.updatedAt
    delYn: str = MaintenanceField.delYn