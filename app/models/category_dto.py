from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId
from pydantic.alias_generators import to_camel


# projection = { "_id": 1, "work_type": 1, "sales_representative_nm": 1, "company_nm": 1, "contract_date": 1, "product_family": 1}
class ResponseCategoryModel(BaseModel):
       id: str = Field(alias='_id')
       contract_title: str = Field(alias='categoryTitle')
       company_id: str = Field(alias='companyId')
       inflow_path: str = Field(alias='inflowPath')
       sales_representative_nm: Optional[str] = Field(None, alias='salesManager')
       contract_date: datetime = Field(alias='contractDate')
       model_config = ConfigDict(
            extra='allow',
            from_attributes=True,
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_encoders={ObjectId: str},
            alias_generator=to_camel
            )