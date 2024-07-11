from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class ServiceDeviceField:
    companyId = Field(
        description="고객사 ID"
    )
    deviceNm = Field(
        description="장비명",
        example="web-12, SQL-golf1",
        min_length=1
    )
    deviceType = Field(
        description="장비 타입",
        example="VM, MSSQLmi",
        min_length=1
    )
    publicIP = Field(
        description="장비 외부 IP",
        example="211.0.0.1",
        pattern=r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    )
    privateIP = Field(
        description="장비 내부 IP",
        example="10.0.0.1",
        pattern=r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    )
    createdAt = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now()
    )
    updatedAt = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    delYn = Field(
        description="삭제된 여부",
        default="N"
    )

class ServiceDeviceDTO(BaseModel):
    _id: str
    companyId: str = ServiceDeviceField.companyId
    deviceNm: str = ServiceDeviceField.deviceNm
    deviceType: str = ServiceDeviceField.deviceType
    publicIP: str = ServiceDeviceField.publicIP
    privateIP: str = ServiceDeviceField.privateIP
    createdAt: datetime = ServiceDeviceField.createdAt
    updatedAt: datetime = ServiceDeviceField.updatedAt
    delYn: str = ServiceDeviceField.delYn