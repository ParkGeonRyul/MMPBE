from pydantic import BaseModel, Field, ConfigDict
from utils.pymongo_object_id import PyObjectId

from datetime import datetime
from bson import ObjectId
from typing import Optional
from utils.snake_by_camel import *

class LoginLogModel(BaseModel):
    log_in_out: str = Field(
        description="LOGIN/LOGOUT",
        alias="loginInOut"
    )
    user_email: str = Field(
        description="접속자 이메일",
        alias="userEmail"
    )
    user_agent: str = Field(
        description="접속자 PC정보",
        alias="userAgent"
    )
    client_ip: str = Field(
        description="접속자 IP정보",
        alias="clientIP"
    )
    success_YN: str = Field(
        description="성공 여부",
        alias="successYN"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="접속 날짜"
    )
    
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "log_in_out": "LOGIN",
                "user_email": "gildong.hong@mavencloudserivce.com",
                "user_agent": "접속자 PC정보",
                "client_ip": "접속자 IP정보",
                "success_YN": "Y",
                "created_at": "2024-09-09 12:00:00"
            }
        }
    )