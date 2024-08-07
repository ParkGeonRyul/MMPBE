from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId
from pydantic.alias_generators import to_camel


class ResponseOfUserModel(BaseModel):
       id: str = Field(alias='_id')
       company_id: str = Field(alias='companyId')
       product_family: str = Field(alias='productFamily')
       sales_manager: Optional[str] = Field(None, alias='salesManager')
       created_at: Optional[str] = Field(None, alias='createdAt')
       model_config = ConfigDict(
            extra='allow',
            from_attributes=True,
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_encoders={ObjectId: str},
            alias_generator=to_camel
            )

# projection = { "_id": 1, "work_type": 1, "sales_manager": 1, "company_nm": 1, "contract_date": 1, "product_family": 1}
class ResponseOfAdminModel(BaseModel):
       id: str = Field(alias='_id')
       work_type: str = Field(alias='workType')
       company_id: str = Field(alias='companyNm')
       product_family: str = Field(alias='productFamily')
       sales_manager: Optional[str] = Field(None, alias='salesManager')
       contract_date: datetime = Field(alias='contractDate')
       model_config = ConfigDict(
            extra='allow',
            from_attributes=True,
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_encoders={ObjectId: str},
            alias_generator=to_camel
            )