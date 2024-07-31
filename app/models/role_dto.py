from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class RoleField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    role_nm = Field(
        description="역할 이름",
        alias="roleNm"
    )

class roldModel(BaseModel):
    role_nm: str = RoleField.role_nm
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "roleNm": "역할 이름"
            }
        }
    )

class RoleCollection(BaseModel):
    roles: List[roldModel]