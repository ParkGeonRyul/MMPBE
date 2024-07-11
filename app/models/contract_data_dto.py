from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class ContractDataField:
    userId = Field(
        description="고객 ID"
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
    createdAt = Field(
        description="생성 날짜(UTC + 0), 임시저장 상태일 때는 NULL 처리",
        default=None
    )
    updatedAt = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    delYn = Field(
        description="삭제된 여부",
        default="N"
    )

class ContractDataDTO(BaseModel):
    _id: str
    userId: str = ContractDataField.userId
    title: str = ContractDataField.title
    content: str = ContractDataField.content
    file: str = ContractDataField.file
    contractDt: datetime = ContractDataField.contractDt
    approvalYn: str = ContractDataField.approvalYn
    createdAt: datetime = ContractDataField.createdAt
    updatedAt: datetime = ContractDataField.updatedAt
    delYn: str = ContractDataField.delYn