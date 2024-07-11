from datetime import datetime

from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List
from typing_extensions import Annotated


class RoleField:
    roleId = Field(
        description="역할 ID"
    ) 
    roleNm = Field(
        description="역할 이름"
    )

class roldDTO(BaseModel):
    _id: str
    roldId: int = RoleField.roleId
    roleNm: str = RoleField.roleNm