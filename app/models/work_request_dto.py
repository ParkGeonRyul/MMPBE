from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class WorkRequestField:
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

class WorkRequestDTO(BaseModel):
    _id: str
    userId: str = WorkRequestField.userId
    deviceNm: str = WorkRequestField.deviceNm
    contactNm: str = WorkRequestField.contactNm
    requestTitle: str = WorkRequestField.requestTitle
    customerNm: str = WorkRequestField.customerNm
    requestDt: datetime = WorkRequestField.requestDt
    workContent: str = WorkRequestField.workContent
    file: str = WorkRequestField.file
    status: str = WorkRequestField.status
    acceptorNm: str = WorkRequestField.acceptorNm
    regYn: str = WorkRequestField.regYn
    createdAt: datetime = WorkRequestField.createdAt
    updatedAt: datetime = WorkRequestField.updatedAt
    delYn: str = WorkRequestField.delYn