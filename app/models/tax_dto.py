from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class TaxField:
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

class TaxDTO(BaseModel):
    _id: str
    userId: str = TaxField.userId
    taxAmt: int = TaxField.taxAmt
    taxDt: datetime = TaxField.taxDt