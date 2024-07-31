from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class authFields:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    access_token = Field(
        description="회사 이름",
        examples="메이븐클라우드서비스"
    )
    refresh_token = Field(
        description="회사 이름",
        examples="메이븐클라우드서비스"
    )


class CompanyModel(BaseModel):
    id: Optional[PyObjectId] = authFields.id
    access_token: str = authFields.access_token
    refresh_token: str = authFields.refresh_token
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "access_token": "sEcRet",
                "refresh_token": "SeCrEt"
            }
        }
    )