from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class companyFields:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    companyNm = Field(
        description="회사 이름",
        examples="메이븐클라우드서비스"
    )

class companyModel(BaseModel):
    id: Optional[PyObjectId] = companyFields.id
    companyNm: str = companyFields.companyNm
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyNm": "메이븐클라우드서비스"
            }
        }
    )

class updateCompanyModel(BaseModel):
    companyNm: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyNm": "메이븐클라우드서비스"
            }
        }
    )

class CompanyCollection(BaseModel):
    companys: List[companyModel]