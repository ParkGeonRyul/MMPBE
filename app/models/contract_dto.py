from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class contractField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
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
        description="제품 집단",
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
        description="작업 시작 날짜(UTC + 0)"
    )
    contactEndDt = Field(
        description="작업 종료 날짜(UTC + 0)"
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

class updateContractModel(BaseModel):
    id: Optional[PyObjectId] = contractField.id
    companyId : str = contractField.companyId
    workType : str = contractField.workType
    tenantId : str = contractField.tenantId
    inflowPath : str = contractField.inflowPath
    customerLevel : str = contractField.customerLevel
    productFamily : str = contractField.productFamily
    contractAmt : int = contractField.contractAmt
    joinService : str = contractField.joinService
    mD : str = contractField.mD
    mM : str = contractField.mH
    mH : str = contractField.mH
    salesManager : str = contractField.salesManager
    techManager : str = contractField.techManager
    taxMail : Optional[str] = contractField.taxMail
    paymentStandard : str = contractField.paymentStandard
    contractDt : datetime = contractField.contractDt
    contractStartDt : datetime = contractField.contractStartDt
    contractEndDt : datetime = contractField.contactEndDt
    createdAt : Optional[datetime] = contractField.createdAt
    updatedAt : Optional[datetime] = contractField.updatedAt
    delYn : Optional[str] = contractField.delYn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "workType": "계약 타입",
                "tenantId": "테넌트 ID",
                "inflowPath": "유입 경로",
                "customerLevel": "고객 단계",
                "productFamily": "제품 집단",
                "contractAmt": "계약 단가",
                "joinService": "서비스 단계",
                "mD": "하루 별 총 작업량",
                "mM": "한 달 별 총 작업량",
                "mH": "1시간 별 총 작업량",
                "salesManager": "판매 담당자",
                "techManager": "기술 담당자",
                "taxMail": "세금 요청 날짜",
                "paymentStandard": "미확인",
                "contractDt": "계약 날짜",
                "contractStartDt": "작업 시작 날짜",
                "contractEndDt": "작업 종료 날짜"
            }
        }
    )

class contractModel(BaseModel):
    companyId : Optional[str] = None
    workType : Optional[str] = None
    tenantId : Optional[str] = None
    inflowPath : Optional[str] = None
    customerLevel : Optional[str] = None
    productFamily : Optional[str] = None
    contractAmt : Optional[int] = None
    joinService : Optional[str] = None
    mD : Optional[str] = None
    mM : Optional[str] = None
    mH : Optional[str] = None
    salesManager : Optional[str] = None
    techManager : Optional[str] = None
    taxMail : Optional[str] = None
    paymentStandard : Optional[str] = None
    contractDt : Optional[datetime] = None
    contractStartDt : Optional[datetime] = None
    contractEndDt : Optional[datetime] = None
    createdAt : Optional[datetime] = None
    updatedAt : Optional[datetime] = None
    delYn : Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "workType": "계약 타입",
                "tenantId": "테넌트 ID",
                "inflowPath": "유입 경로",
                "customerLevel": "고객 단계",
                "productFamily": "제품 집단",
                "contractAmt": "계약 단가",
                "joinService": "서비스 단계",
                "mD": "하루 별 총 작업량",
                "mM": "한 달 별 총 작업량",
                "mH": "1시간 별 총 작업량",
                "salesManager": "판매 담당자",
                "techManager": "기술 담당자",
                "taxMail": "세금 요청 날짜",
                "paymentStandard": "미확인",
                "contractDt": "계약 날짜",
                "contractStartDt": "작업 시작 날짜",
                "contractEndDt": "작업 종료 날짜"
            }
        }
    )


class contractCollection(BaseModel):
    contracts: List[contractModel]