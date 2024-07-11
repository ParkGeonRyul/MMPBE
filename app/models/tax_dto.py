from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class TaxField:
    userId = Field(
        description="고객 ID"
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