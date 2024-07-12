from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class RoleField:
    roleId = Field(
        description="역할 ID(Index)"
    ) 
    roleNm = Field(
        description="역할 이름"
    )

class roldDTO(BaseModel):
    _id: str
    roldId: int = RoleField.roleId
    roleNm: str = RoleField.roleNm