from pydantic import BaseModel, Field, ConfigDict
from utils.pymongo_object_id import PyObjectId

from datetime import datetime
from typing import List
from bson import ObjectId


class TaxField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="고객 ID(ObjectID)",
        alias="userId"
    )
    tax_amt = Field(
        description="과금 내역",
        example="100000",
        ge=0,
        default=0,
        alias="taxAmt"
    )
    tax_date = Field(
        description="과금 날짜(UTC + 0)",
        alias="taxDate"
    )

class TaxModel(BaseModel):
    user_id: str = TaxField.user_id
    tax_amt: int = TaxField.tax_amt
    tax_date: datetime = TaxField.tax_date
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "고객ID(ObjectId)",
                "taxAmt": "과금 내역",
                "taxDate": "과금 날짜(UTC + 0)"
            }
        }
    )

class TaxCollection(BaseModel):
    taxs: List[TaxModel]