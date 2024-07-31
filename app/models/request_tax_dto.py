from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class RequestTaxField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="고객 ID(ObjectID)",
        alias="userId"
    )
    request_date = Field(
        description="요청 날짜(UTC + 0)",
        alias="requestDate"
    )
    content = Field(
        description="요청 내용",
        examples="202301 ~ 202302",
        min_length=1
    )
    status = Field(
        description="요청 진행 상황",
        examples="대기, 완료",
        default="대기"
    )

class CreateRequestTaxModel(BaseModel):
    id: Optional[PyObjectId] = RequestTaxField.id
    user_id: str = RequestTaxField.user_id
    request_date: datetime = RequestTaxField.request_date
    content: str = RequestTaxField.content
    status: Optional[str] = RequestTaxField.status
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "고객ID(ObjectId)",
                "requestDate": "요청 날짜",
                "requestContent": "요청 내용",
                "status": "요청 진행 상황",
            }
        }
    )

class UpdateRequestTaxModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    request_date: Optional[datetime] = None
    request_content: Optional[str] = None
    status: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "request_date": "요청 날짜",
                "request_content": "요청 내용",
                "status": "요청 진행 상황",
            }
        }
    )

class RequestTaxCollection(BaseModel):
    request_taxs: List[CreateRequestTaxModel]