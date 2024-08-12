from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId


class ContractField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    company_id = Field(
        description="회사 ID(ObjectID)",
        alias="companyId"
    )
    work_type = Field(
        description="계약 타입",
        example="라이선스, 프로젝트",
        alias="workType"
    )
    tenant_id = Field(
        description="테넌트 ID값",
        alias="tenantId"
    )
    inflow_path = Field(
        description="유입 경로",
        example="MS(세미나), 인바운드",
        alias="inflowPath"
    )
    customer_level = Field(
        description="고객 단계",
        example="EPG, SMC",
        alias="customerLevel"
    )
    product_family = Field(
        description="제품 집단",
        example="Azure, PowerBI",
        alias="productFamily"
    )
    contract_amt = Field(
        description="계약 가격",
        example="15000",
        ge=0,
        default=0,
        alias="contractAmt"
    )
    join_service = Field(
        description="서비스 단계",
        example="Basic, Pro",
        alias="joinService"
    )
    m_d = Field(
        description="하루 별 총 작업량",
        alias="mD"
    )
    m_m = Field(
        description="한 달 별 총 작업량",
        alias="mM"
    )
    m_h = Field(
        description="1시간 별 총 작업량",
        alias="mH"
    )
    sales_representative_nm = Field(
        description="판매 담당자",
        example="Livy Han, Cho",
        alias="salesRepresentativeNm"
    )
    tech_manager = Field(
        description="기술 담당자",
        example="Aiden, Sun",
        alias="techManager"
    )
    tax_date = Field(
        description="세금 요청 날짜 (UTC +0)",
        default=None,
        alias="taxDate"
    )
    contract_date = Field(
        description="계약 날짜(UTC + 0)",
        alias="contractDate"
    )
    contract_start_date = Field(
        description="작업 시작 날짜(UTC + 0)",
        alias="contractStartDate"
    )
    contact_end_date = Field(
        description="작업 종료 날짜(UTC + 0)",
        alias="contractEndDate"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now()
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=None
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N"
    )

class CreateContractModel(BaseModel):
    company_id : str = ContractField.company_id
    work_type : str = ContractField.work_type
    tenant_id : str = ContractField.tenant_id
    inflow_path : str = ContractField.inflow_path
    customer_level : str = ContractField.customer_level
    product_family : str = ContractField.product_family
    contract_amt : int = ContractField.contract_amt
    join_service : str = ContractField.join_service
    m_d : str = ContractField.m_d
    m_m : str = ContractField.m_h
    m_h : str = ContractField.m_h
    sales_representative_nm: str = ContractField.sales_representative_nm
    tech_manager : str = ContractField.tech_manager
    contract_date : datetime = ContractField.contract_date
    contract_start_date : datetime = ContractField.contract_start_date
    contract_end_date : datetime = ContractField.contact_end_date
    created_at : Optional[datetime] = ContractField.created_at
    updated_at : Optional[datetime] = ContractField.updated_at
    del_yn : Optional[str] = ContractField.del_yn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "companyId": "고객사 ID(ObjectId)",
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
                "taxDate": "세금 요청 날짜",
                "contractDate": "계약 날짜",
                "contractStartDate": "작업 시작 날짜",
                "contractEndDate": "작업 종료 날짜"
            }
        }
    )

class UpdateContractModel(BaseModel):
    company_id : Optional[str] = None
    work_type : Optional[str] = None
    tenant_id : Optional[str] = None
    inflow_path : Optional[str] = None
    customer_level : Optional[str] = None
    product_family : Optional[str] = None
    contract_amt : Optional[int] = None
    join_service : Optional[str] = None
    m_d : Optional[str] = None
    m_m : Optional[str] = None
    m_h : Optional[str] = None
    sales_representative_nm : Optional[str] = None
    tech_manager : Optional[str] = None
    tax_mail : Optional[str] = None
    payment_standard : Optional[str] = None
    contract_date : Optional[datetime] = None
    contract_start_date : Optional[datetime] = None
    contract_end_date : Optional[datetime] = None
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    del_yn : Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "company_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
                "work_type": "계약 타입",
                "tenant_id": "테넌트 ID",
                "inflow_path": "유입 경로",
                "customer_level": "고객 단계",
                "product_family": "제품 집단",
                "contract_amt": "계약 단가",
                "join_service": "서비스 단계",
                "m_d": "하루 별 총 작업량",
                "m_m": "한 달 별 총 작업량",
                "m_h": "1시간 별 총 작업량",
                "sales_manager": "판매 담당자",
                "tech_manager": "기술 담당자",
                "tax_mail": "세금 요청 날짜",
                "payment_standard": "미확인",
                "contract_date": "계약 날짜",
                "contract_start_date": "작업 시작 날짜",
                "contract_end_date": "작업 종료 날짜"
            }
        }
    )


class ContractCollection(BaseModel):
    contracts: List[CreateContractModel]