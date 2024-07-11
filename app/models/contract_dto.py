from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import AfterValidator
from datetime import datetime

from typing import Any, List

from typing_extensions import Annotated


class ContractField:
    companyId = Field(
        description="회사 ID(ObjectID)"
    )
    workType = Field(
        description="계약 타입",
        examples="라이선스, 프로젝트"
    )
    tenantId = Field(
        description="테넌트 ID값"
    )
    inflowPath = Field(
        description="유입 경로",
        examples="MS(세미나), 인바운드"
    )
    customerLevel = Field(
        description="고객 단계",
        examples="EPG, SMC"
    )
    productFamily = Field(
        description="계약 집단",
        examples="Azure, PowerBI"
    )
    contractAmt = Field(
        description="계약 가격",
        examples="15000",
        ge=0,
        default=0
    )
    joinService = Field(
        description="서비스 단계",
        examples="Basic, Pro"
    )
    mD = Field(
        description="하루 별 총 작업량"
    )
    mM = Field(
        description="한 달 별 총 작업량"
    )
    mH = Field(
        description="1시간 별 총 작업량"
    )
    salesManager = Field(
        description="판매 담당자",
        examples="Livy Han, Cho"
    )
    techManager = Field(
        description="기술 담당자",
        examples="Aiden, Sun"
    )
    taxMail = Field(
        description="세금 요청 날짜 (UTC +0)",
        default=None
    )
    paymentStandard = Field(
        description="???(확인필요)"
    )
    contractDt = Field(
        description="계약 날짜(UTC + 0)"
    )
    contractStartDt = Field(
        description="계약 시작 날짜(UTC + 0)"
    )
    contactEndDt = Field(
        description="계약 종료 날짜(UTC + 0)"
    )
    createdAt = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now()
    )
    updatedAt = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    delYn = Field(
        description="삭제된 여부",
        default="N"
    )

class ContractDTO(BaseModel):
    _id: str
    companyId : str = ContractField.companyId
    workType : str = ContractField.workType
    tenantId : str = ContractField.tenantId
    inflowPath : str = ContractField.inflowPath
    customerLevel : str = ContractField.customerLevel
    productFamily : str = ContractField.productFamily
    contractAmt : int = ContractField.contractAmt
    joinService : str = ContractField.joinService
    mD : str = ContractField.mD
    mM : str = ContractField.mH
    mH : str = ContractField.mH
    salesManager : str = ContractField.salesManager
    techManager : str = ContractField.techManager
    taxMail : str = ContractField.taxMail
    paymentStandard : str = ContractField.paymentStandard
    contract_dt : datetime = ContractField.contractDt
    contractStartDt : datetime = ContractField.contractStartDt
    contractEndDt : datetime = ContractField.contactEndDt
    createdAt : datetime = ContractField.createdAt
    updatedAt : datetime = ContractField.updatedAt
    delYn : str = ContractField.delYn