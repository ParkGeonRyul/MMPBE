from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic.alias_generators import to_camel


class ResponseCategoryModel(BaseModel):
       id: str = Field(alias='_id')
       contract_title: str = Field(alias='categoryTitle')
       company_id: str = Field(alias='companyId')
       inflow_path: str = Field(alias='inflowPath')
       sales_representative_nm: Optional[str] = Field(None, alias='salesRepresentativeNm')
       contract_date: datetime = Field(alias='contractDate')
       model_config = ConfigDict(
            extra='allow',
            from_attributes=True,
            populate_by_name=True,
            arbitrary_types_allowed=True,
            json_encoders={ObjectId: str},
            alias_generator=to_camel
            )