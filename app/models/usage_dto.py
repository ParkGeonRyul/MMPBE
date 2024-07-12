from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class UsageField:
    userId = Field(
        description="고객 ID"
    )
    serviceDeviceId = Field(
        description="서비스 장비 ID(ObjectID)"
    )
    cpu = Field(
        description="CPU 사용량",
        examples="10, 80",
        ge=0,
        default=0
    )
    disk = Field(
        description="Disk 사용량",
        examples="10, 50",
        ge=0,
        default=0
    )

class UsageDTO(BaseModel):
    _id: str
    userId: str = UsageField.userId
    serviceDeviceId: str = UsageField.serviceDeviceId
    cpu: int = UsageField.cpu
    disk: int = UsageField.disk