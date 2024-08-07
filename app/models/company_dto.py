from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class CompanyFields:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    company_nm = Field(
        description="회사 이름",
        example="메이븐클라우드서비스",
        alias="companyNm"
    )

class CompanyModel(BaseModel):
    company_nm: str = CompanyFields.company_nm
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyNm": "메이븐클라우드서비스"
            }
        }
    )

class UpdateCompanyModel(BaseModel):
    company_nm: Optional[str] = None
    model_config = ConfigDict(
        extra=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyNm": "메이븐클라우드서비스"
            }
        }
    )

class CompanyCollection(BaseModel):
    companys: List[CompanyModel]