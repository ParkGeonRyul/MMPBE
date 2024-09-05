from pydantic import BaseModel, Field, ConfigDict
from utils.pymongo_object_id import PyObjectId

from datetime import datetime
from typing import List, Optional
from bson import ObjectId


class UsageField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="고객 ID",
        alias="userId"
    )
    service_device_id = Field(
        description="서비스 장비 ID(ObjectID)",
        alias="serviceDeviceId"
    )
    cpu = Field(
        description="CPU 사용량",
        example="10, 80",
        ge=0,
        default=0
    )
    disk = Field(
        description="Disk 사용량",
        example="10, 50",
        ge=0,
        default=0
    )

class UsageModel(BaseModel):
    id: Optional[PyObjectId] = UsageField.id
    user_id: str = UsageField.user_id
    service_device_id: str = UsageField.service_device_id
    cpu: int = UsageField.cpu
    disk: int = UsageField.disk
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "고객ID(ObjectId)",
                "serviceDeviceId": "서비스장비ID(ObjectId)",
                "cpu": "CPU 사용량",
                "disk": "disk 사용량"
            }
        }
    )

class UsageCollection(BaseModel):
    usages: List[UsageModel]