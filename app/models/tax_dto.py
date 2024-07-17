from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class TaxField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    userId = Field(
        description="고객 ID(ObjectID)"
    )
    taxAmt = Field(
        description="과금 내역",
        examples="100000",
        ge=0,
        default=0
    )
    taxDt = Field(
        description="과금 날짜(UTC + 0)"
    )

class TaxModel(BaseModel):
    id: Optional[PyObjectId] = TaxField.id
    userId: str = TaxField.userId
    taxAmt: int = TaxField.taxAmt
    taxDt: datetime = TaxField.taxDt
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "taxAmt": "과금 내역",
                "taxDt": "과금 날짜(UTC + 0)"
            }
        }
    )

class TaxCollection(BaseModel):
    companys: List[TaxModel]