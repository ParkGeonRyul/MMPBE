from pydantic import BaseModel, Field, ConfigDict, ValidationError
from dotenv import load_dotenv
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId
from datetime import datetime, timezone
from pydantic.alias_generators import to_camel

import os

from db.context import work_plan_collection, work_request_collection
from routes._modules.mongo_join import *
from utils.pymongo_object_id import PyObjectId


load_dotenv()

file_url = os.getenv("FILE_URL")


class WorkPlanField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="작업계획서 수신자 id(ObjectID)",
        alias="userId"
    )
    acceptor_id = Field(
        description="작업계획서 발신자 id(ObjectID)",
        min_length=1,
        default=None,
        alias="acceptorId"
    )
    request_id = Field(
        description="작업 요청서 id(ObjectID)",
        min_length=1,
        default=None,
        alias="requestId"
    )
    plan_title = Field(
        description="계획서 제목",
        example="Web DNS 설정",
        min_length=1,
        alias="planTitle"
    )
    plan_content = Field(
        description="계획서 내용",
        min_length=1,
        alias= "planContent"
    )
    plan_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=datetime.now(timezone.utc),
        alias="planDate"
    )
    file_path = Field(
        description="첨부 파일",
        example="Zone파일.zip",
        default=None,
        alias="filePath"
    )
    status = Field(
        description="승인 여부",
        example="요청, 회수, 승인, 반려",
        default="요청",
        alias="status"
    )
    status_content = Field(
        description="승인/반려 내용",
        example="승인내용, 반려사유",
        default=None,
        alias="statusContent"
    )
    created_at = Field(
        description="생성 날짜(UTC + 0)",
        default=datetime.now(timezone.utc),
        alias="createdAt"
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=datetime.now(timezone.utc),
        alias="updatedAt"
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N",
        alias="delYn"
    )

class CreateWorkPlanModel(BaseModel): # fe -> be
    user_id: Optional[str] = WorkPlanField.user_id
    acceptor_id: str = WorkPlanField.acceptor_id
    request_id: str = WorkPlanField.request_id
    plan_title: str = WorkPlanField.plan_title
    plan_content: str = WorkPlanField.plan_content
    plan_date: Optional[datetime] = WorkPlanField.plan_date
    file_path: Optional[str] = WorkPlanField.file_path
    status: Optional[str] = WorkPlanField.status
    status_content : Optional[str] = WorkPlanField.status_content
    created_at: Optional[datetime] = WorkPlanField.created_at
    updated_at: Optional[datetime] = WorkPlanField.updated_at
    del_yn: Optional[str] = WorkPlanField.del_yn
    model_config = ConfigDict(
        from_attributes = True,
        populate_by_name = True,
        json_encoders = {ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra = {
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "acceptorId": "작업요청자 수신자 id(ObjectID)",
                "requestId": "작업계획서(ObjectID)",
                "planTitle": "계획서 제목",
                "planContent": "계획서 내용",
                "planDate": "2024-08-05 00:00:00",
                "filePath": "파일ID(ObjectID)",
                "status": "요청",
                "statusContent": "승인내용",
                "createdAt": "2024-08-05 00:00:00",
                "updatedAt": "2024-08-05 00:00:00"
            }
        }
    )

class UpdateWorkPlanModel(BaseModel):
    user_id: Optional[str] = WorkPlanField.user_id
    acceptor_id: str = WorkPlanField.acceptor_id
    request_id: str = WorkPlanField.request_id
    plan_title: str = WorkPlanField.plan_title
    plan_content: str = WorkPlanField.plan_content
    plan_date: Optional[datetime] = WorkPlanField.plan_date
    file_path: Optional[str] = WorkPlanField.file_path
    status: Optional[str] = WorkPlanField.status
    status_content : Optional[str] = WorkPlanField.status_content
    updated_at: Optional[datetime] = WorkPlanField.updated_at
    del_yn: Optional[str] = WorkPlanField.del_yn
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "acceptorId": "작업요청자 수신자 id(ObjectID)",
                "requestId": "작업계획서(ObjectID)",
                "planTitle": "계획서 제목",
                "planContent": "계획서 내용",
                "planDate": "2024-08-05 00:00:00",
                "filePath": "파일ID(ObjectID)",
                "status": "요청",
                "statusContent": "승인내용",
                "updatedAt": "2024-08-05 00:00:00"
            }
        }
    )

class  UpdatePlanStatusAcceptModel(BaseModel):
    status: Optional[str] = None
    status_content: Optional[str] = WorkPlanField.status_content
    updated_at: Optional[datetime] = WorkPlanField.updated_at
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

class  UpdatePlanStatusModel(BaseModel):
    status: Optional[str] = None
    updated_at: Optional[datetime] = WorkPlanField.updated_at
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "status": "승인",
            }
        }
    )

class DeletePlanTempraryModel(BaseModel):
    ids: List[str]

class UpdateDelYnWorkPlanModel(BaseModel):
    plan_id: str = Field(description="작업 요청 ID", alias="requestId")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "plan_id": "6690cf7fa4897bf6b90541c1(ObjectId)",
            }
        }
    )

class ResponsePlanListModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(alias="userId")
    plan_title: str = Field(alias="planTitle")
    wr_title: str = Field(alias="wrTitle")
    acceptor_id: Optional[str] = Field(None, alias="acceptorId")
    acceptor_nm: Optional[str] = Field(None, alias="acceptorNm")
    company_nm: Optional[str] = Field(None, alias="companyNm")
    requestor_nm: Optional[str] = Field(None, alias="requestorNm")
    plan_date: str = Field(alias="planDate")
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

    
class ResponsePlanDtlModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(alias="requestorId")
    request_id: str = Field(alias="requestId")
    wr_title: str = Field(alias="wrTitle")
    requestor_data: dict
    acceptor_data: dict
    plan_title: str = Field(alias='planTitle')
    plan_content: str = Field(alias='planContent')
    plan_date: datetime = Field(alias="planDate")
    file: Optional[dict] = None
    status: str
    status_content: Optional[str] = Field(None, alias="statusContent")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
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

class ResponseRequestCategoryModel(BaseModel):
    id: str = Field(alias="_id")
    wr_title: str = Field(alias="wrTitle")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
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
       
async def get_list(match: dict, projection: dict, skip: int, limit: int):
    request = ("workRequest", "request", "request", "request", False)
    acceptor = ("users", "acceptor", "acceptor", "acceptor", False)
    user = ("users", "user", "user", "user", False)
    company = ("company", "company", "acceptor_field.company", "company", False)
    set_data = {                    
                    "acceptor_id": {"$toString": "$acceptor_field._id"},
                    "acceptor_nm": "$acceptor_field.user_nm",
                    "requestor_nm": "$user_field.user_nm",
                    "wr_title": "$request_field.wr_title",
                    "company_nm": "$company_field.company_nm"
                }
    
    pipeline = set_pipeline(match, projection, [request, acceptor, user, company], set_data, skip, limit)

    results = work_plan_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        if match['plan_date'] == {'$ne': None}:
            item['plan_date'] = str(item['plan_date'])
        model_instance = ResponsePlanListModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content

async def get_category_list(match: dict, projection: dict):
    contract = ("contract", "solution", "solution", "contract", False)
    customer = ("users", "customer", "customer", "customer", False)
    company = ("company", "company", "customer_field.company", "company", False)
    set_data = {                    
                    "sales_representative_nm": "$contract_field.sales_representative_nm",
                    "contract_title": "$contract_field.contract_title",
                    "customer_nm": "$customer_field.user_nm",
                    "company_nm": "$company_field.company_nm"
                }
    pipeline = set_pipeline(match, projection, [contract, customer, company], set_data, None, None)
    results = work_request_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        item['wr_date'] = str(item['wr_date'])

        model_instance = ResponseRequestCategoryModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content

async def get_dtl(match: dict, projection: dict):
    acceptor = ("users", "acceptor", "acceptor", "acceptor", False)
    user = ("users", "user", "user", "user", False)
    request = ("workRequest", "request", "request", "request", False)
    files = ("files", "file", "file", "file", True)
    company = ("company", "company", "acceptor_field.company", "company", False)
    set_data = {                    
                    "wr_title": "$request_field.wr_title",
                    "requestor_data": {
                    "_id": "$user_field._id",
                    "name": "$user_field.user_nm",
                    "rank": "$user_field.rank",
                    "email": "$user_field.email",
                    "companyContact": "$user_field.company_contact",
                    "mobileContact": "$user_field.mobile_contact"
                    },
                    "acceptor_data": {
                        "_id": "$acceptor_field._id",
                        "name": "$acceptor_field.user_nm",
                        "rank": "$acceptor_field.rank",
                        "companyId": "$company_field._id",
                        "companyNm": "$company_field.company_nm",
                        "email": "$acceptor_field.email",
                        "companyContact": "$acceptor_field.company_contact",
                        "mobileContact": "$acceptor_field.mobile_contact",
                    },
                    "files": { "$ifNull": [{
                        "id": "$file_path",
                        "name": {"$ifNull": ["$file_field.origin", None]},
                        "url": {"$concat": [file_url,"$file_field.user_id","/", "$file_field.uuid"]},
                        "size": {"$toString": "$file_field.size"},
                        "type": "$file_field.extension"
                    }, None]}
                }
    
    pipeline = set_pipeline(match, projection, [request, acceptor, user, files, company], set_data, None, None)

    result = work_plan_collection.aggregate(pipeline)
    content=[]
    for item in result:
        item['_id'] = str(item['_id'])
        item['plan_date'] = str(item['plan_date'])
        model_instance = ResponsePlanDtlModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content[0]