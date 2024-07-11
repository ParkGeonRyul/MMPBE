from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class CompanyFields:
    companyNm = Field(
        description = "회사 이름",
        examples = "메이븐클라우드서비스"
        # NOT NULL 테스트
    )

class CompanyDTO(BaseModel):
    _id: str
    componyNm : str = CompanyFields.companyNm