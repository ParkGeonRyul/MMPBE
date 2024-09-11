from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from pydantic.alias_generators import to_camel
from dotenv import load_dotenv

import os

from db.context import work_request_collection, contract_collection
from routes._modules.mongo_join import *
from utils.pymongo_object_id import PyObjectId
from utils.snake_by_camel import convert_keys_to_camel_case

load_dotenv()

file_url = os.getenv("FILE_URL")

class WorkRequestField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    company_id = Field(
        description="고객사 ID(ObjectID)",
        alias = "companyId"
    )
    customer_id = Field(
        description="고객 ID(ObjectID)",
        alias="customerId"
    )
    solution_id = Field(
        description="계약 ID(ObjectID)",
        alias="solutionId"
    )
    device_type_id = Field(
        description="Device 타입 ID(ObjectID)",
        default=None,
        alias="deviceTypeId"
    )
    wr_title = Field(
        description="작업 요청 제목",
        example="Web DNS 설정",
        min_length=1,
        alias="wrTitle"
    )
    content = Field(
        description="작업 요청 내용",
        example="Web DNS 설정 및....",
        min_length=1
    )
    wr_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=None,
        alias="wrDate"
    )
    file_path = Field(
        None,
        description="파일 경로",
        alias="filePath"
    )
    status = Field(
        description="요청 상태",
        example="요청, 회수, 승인, 반려",
        default="요청"
    )
    status_content = Field(
        description="상태 관련 답변",
        default=None,
        alias="statusContent"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now(timezone.utc)
    )
    updated_at = Field(
        description="정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=datetime.now(timezone.utc)
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N"
    )

class ResponseRequestListModel(BaseModel):
    id: str = Field(alias="_id")
    wr_title: str = Field(alias="wrTitle")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
    contract_title: Optional[str] = Field(alias="contractTitle")
    customer_id: Optional[str] = Field(None, alias="customerId")
    customer_nm: Optional[str] = Field(None, alias="customerNm")
    company_nm: Optional[str] = Field(None, alias="companyNm")
    wr_date: Optional[str] = Field(None, alias="wrDate")
    status: str
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        alias_generator=to_camel,
        json_schema_extra={
            "example": {
                "_id": "ObjectId",
                "requestTitle": "요청 제목",
                "salesRepresentative": "영업담당자",
                "wrDate": "임시저장 == NULL",
                "status": "승인, 반려, 요청, 회수"
            }
        }
    )
    
class ResponseRequestDtlModel(BaseModel):
    id: str = Field(alias="_id")
    solution_id: str = Field(alias="solutionId")
    wr_title: str = Field(alias="wrTitle")
    customer_id: str = Field(alias="customerId")
    customer_nm: str = Field(alias="customerNm")
    sales_representative_id: str = Field(alias="salesRepresentativeId")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
    company_id: Optional[str] = Field(None, alias="companyId")
    company_nm: Optional[str] = Field(None, alias="companyNm")
    wr_date: Optional[str] = Field(None, alias="wrDate")
    content: Optional[str]
    status: Optional[str]
    status_content: Optional[str] = Field(alias="statusContent")
    file: dict = Field(None)
    model_config = ConfigDict(
        extra='allow',
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        alias_generator=to_camel,
        json_schema_extra={
            "example": {
                "_id": "ObjectId",
                "wrTitle": "요청 제목",
                "customerId": "고객 ID(ObjectId)",
                "salesRepresentativeId": "판매 담당자 ID",
                "salesRepresentativeNm": "판매 담당자 이름",
                "companyId": "고객사 ID(ObjectId)",
                "companyNm": "고객사 이름",
                "wrDate": "작업 요청 날짜",     
                "content": "요청 내용",
                "status": "요청 상태",
                "statusContent": "상태 관련 답변",
                "filePath": "파일 경로"
            }
        }
    )

class ResponseRequestCategoryModel(BaseModel):
       id: str = Field(alias='_id')
       contract_title: str = Field(alias='categoryTitle')
       company_id: str = Field(alias='companyId')
       inflow_path: str = Field(alias='inflowPath')
       sales_representative_id: str = Field(alias='salesRepresentativeId')
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

class CreateWorkRequestModel(BaseModel): # fe -> be
    solution_id: str = WorkRequestField.solution_id # 계약 ID
    wr_title: str = WorkRequestField.wr_title # 필수
    content: str = WorkRequestField.content
    wr_date: Optional[datetime] = WorkRequestField.wr_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    status: Optional[str] = WorkRequestField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
    status_content: Optional[str] = WorkRequestField.status_content
    created_at: Optional[datetime] = WorkRequestField.created_at # 최초 이후 수정이 안 됨
    del_yn: Optional[str] = WorkRequestField.del_yn # 시스템 관리자를 위한
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "solutionId": "계약 ID(ObjectID)",
                "wrTitle": "작업 요청 제목",
                "content": "작업 요청 내용",
                "wrDate": "작업 요청 날짜"
            }
        }
    )

class  UpdateWorkRequestModel(BaseModel):
    id: str = WorkRequestField.id
    solution_id: Optional[str] = WorkRequestField.solution_id # 계약 ID
    wr_title: Optional[str] = WorkRequestField.wr_title # 필수
    content: Optional[str] = WorkRequestField.content
    wr_date: Optional[datetime] = WorkRequestField.wr_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    status: Optional[str] = WorkRequestField.status # 승인, 반려, 요청, 회수(사용자, 시스템 관리자만 볼 수 있음)
    status_content: Optional[str] = WorkRequestField.status_content
    file_path: Optional[str] = WorkRequestField.file_path
    updated_at: datetime = WorkRequestField.updated_at # 업데이트 된 날짜(수정 불가)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "solutionId": "계약 ID(ObjectID)",
                "wrTitle": "작업 요청 제목",
                "content": "작업 요청 내용",
                "wrDate": "작업 요청 날짜",
                "status": "요청 상태",
                "statusContent": "상태 관련 답변",
                "filePath": "파일 경로"
            }
        }
    )

class DeleteRequestTempraryModel(BaseModel):
    ids: List[str]


class UpdateRequestStatusAcceptModel(BaseModel):
    status: Optional[str] = None
    status_content: Optional[str] = WorkRequestField.status_content
    updated_at: Optional[str]= WorkRequestField.updated_at
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "status": "승인",
                "statusContent": "승인내용",
            }
        }
    )

async def get_categoty_list(match: dict, projection: dict):
    sales_representative = ("users", "user", "sales_representative", "sales_representative", False)
    set_data = {
        "sales_representative_id": "$sales_representative_field._id",
        "sales_representative_nm": "$sales_representative_field.user_nm"
    }
    pipeline = set_pipeline(match, projection, [sales_representative], set_data, None, None)
    results = contract_collection.aggregate(pipeline)
    content = []
    for item in results:
        item['_id'] = str(item['_id'])
        item['sales_representative_id'] = str(item['sales_representative_id'])
        model_instance = ResponseRequestCategoryModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
    
    return content
        

async def get_list(match: dict, projection: dict, skip: int, limit: int):
    contract = ("contract", "solution", "solution", "contract", False) #collection key value"field_nm allow_empty
    sales_representative = ("users", "user", "contract_field.sales_representative", "sales_representative", False)
    customer = ("users", "customer", "customer", "customer", False)
    company = ("company", "company", "customer_field.company", "company", False)
    set_data = {                    
                    "sales_representative_nm": "$sales_representative_field.user_nm",
                    "contract_title": "$contract_field.contract_title",
                    "customer_nm": "$customer_field.user_nm",
                    "company_nm": "$company_field.company_nm"
                }
    pipeline = set_pipeline(match, projection, [contract, sales_representative, customer, company], set_data, skip, limit)
    results = work_request_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        if match['wr_date'] == {'$ne': None}:
            item['wr_date'] = str(item['wr_date'])

        model_instance = ResponseRequestListModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content

async def get_dtl(match: dict, projection: dict):
    contract = ("contract", "solution", "solution", "contract", False)
    sales_representative = ("users", "user", "contract_field.sales_representative", "sales_representative", False)
    customer = ("users", "customer", "customer", "customer", False)
    files = ("files", "file", "file", "file", True)
    company = ("company", "company", "customer_field.company", "company", False)
    set_data = {                  
                    "sales_representative_id": "$sales_representative_field._id", 
                    "sales_representative_nm": "$sales_representative_field.user_nm",
                    "customer_nm": "$customer_field.user_nm",
                    "company_id": "$customer_field.company_id",
                    "company_nm": "$company_field.company_nm",
                    "file": { "$ifNull": [
                        {
                        "id": "$file_path",
                        "name": {"$ifNull": ["$file_field.origin", None]},
                        "url": {"$concat": [file_url,"$file_field.user_id","/", "$file_field.uuid"]},
                        "size": {"$toString": "$file_field.size"},
                        "type": "$file_field.extension"
                        }, None]}
                }
    pipeline = set_pipeline(match, projection, [contract, sales_representative, customer, files, company], set_data, None, None)    
    result = work_request_collection.aggregate(pipeline)
    content=[]
    for item in result:
        item['_id'] = str(item['_id'])
        item['wr_date'] = str(item['wr_date'])
        model_instance = ResponseRequestDtlModel(**item)        
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content[0]