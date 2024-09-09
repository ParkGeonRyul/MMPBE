from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime
from bson import ObjectId
from typing import Optional
from utils.snake_by_camel import *

class WorkLogModel(BaseModel):
    path : str = Field(
        description="호출 경로",
        alias="path"
    )
    method : str = Field(
        description="호출 method",
        alias="method"
    )
    user_agent : str = Field(
        description="접속자 PC정보",
        alias="userAgent"
    )
    client_ip : str = Field(
        description="접속자 IP정보",
        alias="clientIp"
    )
    user_id: str = Field(
        description="사용자 아이디",
        alias = "userId"
    )
    exception_result: Optional[str] = Field(
        description="401 error | null",
        alias = "exceptionResult"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="접속 날짜",
    )
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "path": "/test/test",
                "method": "get",
                "user_agent": "접속자 PC정보",
                "client_ip": "접속자 IP정보",
                "user_id": "사용자 아이디",
                "exception_result": "401 error",
                "created_at": "2024-09-09 12:00:00"
            }
        }
    )