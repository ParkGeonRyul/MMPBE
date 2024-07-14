from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class ServiceDeviceField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    companyId = Field(
        description="고객사 ID(ObjectID)"
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

class ServiceDeviceModel(BaseModel):
    id: Optional[PyObjectId] = ServiceDeviceField.id
    companyId: str = ServiceDeviceField.companyId
    deviceNm: str = ServiceDeviceField.deviceNm
    deviceType: str = ServiceDeviceField.deviceType
    publicIP: str = ServiceDeviceField.publicIP
    privateIP: str = ServiceDeviceField.privateIP
    createdAt: Optional[datetime] = ServiceDeviceField.createdAt
    updatedAt: Optional[datetime] = ServiceDeviceField.updatedAt
    delYn: Optional[str] = ServiceDeviceField.delYn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "deviceNm": "장비 이름",
                "publicIP": "장비 외부 IP",
                "privateIP": "장비 내부 IP"
            }
        }
    )

class ServiceDeviceModel(BaseModel):
    id: Optional[PyObjectId] = None
    companyId: Optional[str] = None
    deviceNm: Optional[str] = None
    deviceType: Optional[str] = None
    publicIP: Optional[str] = None
    privateIP: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    delYn: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "deviceNm": "장비 이름",
                "publicIP": "장비 외부 IP",
                "privateIP": "장비 내부 IP"
            }
        }
    )