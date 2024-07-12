from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class RequestTaxField:
    userId = Field(
        description="고객 ID(ObjectID)"
    )
    requestDt = Field(
        description="요청 날짜(UTC + 0)"
    )
    requestContent = Field(
        description="요청 내용",
        examples="202301 ~ 202302",
        min_length=1
    )
    status = Field(
        description="요청 진행 상황",
        examples="대기, 완료"
    )

class RequestTaxDTO(BaseModel):
    _id: str
    userId: str = RequestTaxField.userId
    requestDt: datetime = RequestTaxField.requestDt
    requestContent: str = RequestTaxField.requestContent
    status: str = RequestTaxField.status