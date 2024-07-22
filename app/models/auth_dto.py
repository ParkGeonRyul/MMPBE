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
    accessToken = Field(
        description="회사 이름",
        examples="메이븐클라우드서비스"
    )
    refreshToken = Field(
        description="회사 이름",
        examples="메이븐클라우드서비스"
    )


class CompanyModel(BaseModel):
    id: Optional[PyObjectId] = authFields.id
    accessToken: str = authFields.accessToken
    refreshToken: str = authFields.refreshToken
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "accessToken": "sEcRet",
                "refreshToken": "SeCrEt"
            }
        }
    )