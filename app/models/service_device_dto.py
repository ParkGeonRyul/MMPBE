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
    company_id = Field(
        description="고객사 ID(ObjectID)"
    )
    device_nm = Field(
        description="장비명",
        example="web-12, SQL-golf1",
        min_length=1
    )
    device_type = Field(
        description="장비 타입",
        example="VM, MSSQLmi",
        min_length=1
    )
    public_ip = Field(
        description="장비 외부 IP",
        example="211.0.0.1",
        pattern=r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    )
    private_ip = Field(
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
    del_yn = Field(
        description="삭제된 여부",
        default="N"
    )

class ServiceDeviceModel(BaseModel):
    id: Optional[PyObjectId] = ServiceDeviceField.id
    company_id: str = ServiceDeviceField.company_id
    device_nm: str = ServiceDeviceField.device_nm
    device_type: str = ServiceDeviceField.device_type
    public_ip: str = ServiceDeviceField.public_ip
    private_ip: str = ServiceDeviceField.private_ip
    createdAt: Optional[datetime] = ServiceDeviceField.createdAt
    updatedAt: Optional[datetime] = ServiceDeviceField.updatedAt
    del_yn: Optional[str] = ServiceDeviceField.del_yn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "company_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "device_nm": "장비 이름",
                "public_ip": "장비 외부 IP",
                "private_ip": "장비 내부 IP"
            }
        }
    )

class ServiceDeviceModel(BaseModel):
    id: Optional[PyObjectId] = None
    company_id: Optional[str] = None
    device_nm: Optional[str] = None
    device_type: Optional[str] = None
    public_ip: Optional[str] = None
    private_ip: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    del_yn: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "company_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "device_nm": "장비 이름",
                "public_ip": "장비 외부 IP",
                "private_ip": "장비 내부 IP"
            }
        }
    )

class ServiceDeviceCollection(BaseModel):
    service_devices: List[ServiceDeviceModel]