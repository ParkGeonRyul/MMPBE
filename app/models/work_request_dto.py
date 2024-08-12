from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic.alias_generators import to_camel

import json

from utils.pymongo_object_id import PyObjectId


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
        alias="requestTitle"
    )
    content = Field(
        description="작업 요청 내용",
        example="Web DNS 설정 및....",
        min_length=1,
        alias="requestContent"
    )
    wr_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=None,
        alias="requestDate"
    )
    file_path = Field(
        description="파일 경로",
        default=None
    )
    status = Field(
        description="요청 상태",
        example="요청, 회수, 승인, 반려",
        default="요청"
    )
    status_content = Field(
        description="상태 관련 답변",
        default=None
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

class CreateWorkRequestModel(BaseModel): # fe -> be
    company_id: str = WorkRequestField.company_id # id 
    customer_id: str = WorkRequestField.customer_id # 담당자 ID
    solution_id: str = WorkRequestField.solution_id # 계약 ID
    wr_title: str = WorkRequestField.wr_title # 필수
    content: str = WorkRequestField.content
    wr_date: Optional[datetime] = WorkRequestField.wr_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    status: Optional[str] = WorkRequestField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
    status_content: Optional[str] = WorkRequestField.status_content
    file_path: str = WorkRequestField.file_path
    created_at: Optional[datetime] = WorkRequestField.created_at # 최초 이후 수정이 안 됨
    updated_at: Optional[datetime] = WorkRequestField.updated_at 
    del_yn: Optional[str] = WorkRequestField.del_yn # 시스템 관리자를 위한
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "requestPlanId": "작업계획서(ObjectID)",
                "contactNm": "담당자 이름(Maven)",
                "wrTitle": "요청 제목",
                "customerNm": "고객 이름",
                "wrDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "statusContent": "요청 답변 내용(Default Null)",
                "delYn": "삭제 여부"
            }
        }
    )

class  UpdateWorkRequestModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    device_nm: Optional[str] = None
    contact_nm: Optional[str] = None
    wr_title: Optional[str] = None
    customer_nm: Optional[str] = None
    wr_date: Optional[datetime] = None
    content: Optional[str] = None
    file: Optional[str] = None
    status: Optional[str] = None
    acceptor_nm: Optional[str] = None
    reg_yn: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    del_yn: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "requestPlanId": "작업계획서(ObjectID)",
                "contactNm": "담당자 이름(Maven)",
                "wrTitle": "요청 제목",
                "customerNm": "고객 이름",
                "wrDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "statusContent": "요청 답변 내용(Default Null)",
                "delYn": "삭제 여부"
            }
        }
    )

class DeleteRequestTempraryModel(BaseModel):
    ids: List[str]

class ResponseRequestListModel(BaseModel):
    id: str = Field(alias="_id")
    wr_title: str = Field(alias="wrTitle")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
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
    wr_title: str = Field(alias="wrTitle")
    company_id: str = Field(alias="companyId")
    customer_id: str = Field(alias="customerId")
    customer_nm: str = Field(alias="customerNm")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
    company_id: Optional[str] = Field(None, alias="companyId")
    company_nm: Optional[str] = Field(None, alias="companyNm")
    wr_date: Optional[str] = Field(None, alias="wrDate")
    file_path: Optional[str] = Field(alias="filePath")
    status: str
    status_content: Optional[str] = Field(alias="statusContent")
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

async def get_list(match: dict, projection: dict, db_collection: any, response_model: any): #skip: int, 
    pipeline = [
            {
                "$match": match,
            },
            {
                "$lookup": {
                    "from": "contract",
                    "let": { "solutionId": "$solution_id" },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [ {"$toString": "$_id"}, "$$solutionId"]
                                }
                            }
                        }
                    ],
                    "as": "contract_field"
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "let": { "customerId": "$customer_id" },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [ {"$toString": "$_id"}, "$$customerId"]
                                }
                            }
                        }
                    ],
                    "as": "customer_field"
                  }
            },
            {
                "$unwind": "$contract_field"
            },
            {
                "$unwind": "$customer_field"
            },
            {
                "$lookup": {
                    "from": "company",
                    "let": { "companyId": "$customer_field.company_id" },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [ {"$toString": "$_id"}, "$$companyId"]
                                }
                            }
                        }
                    ],
                    "as": "company_field"
                  }
            },
            {
                "$unwind": "$company_field"
            },
            # projection = {"_id": 1, "wr_title": 1, "sales_representative_nm": 1, "customer_nm": 1, "company_nm": 1, "wr_date": 1, "status": 1}
            {
                "$set": {
                    "sales_representative_nm": "$contract_field.sales_representative_nm",
                    "customer_nm": "$customer_field.user_nm",
                    "company_nm": "$company_field.company_nm"
                }
            },
            {
                "$project": projection
            }
          ]
    results = db_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        if match['wr_date'] == {'$ne': None}:
            item['wr_date'] = str(item['wr_date'])

        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
    # numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(content)]

    return content

async def get_dtl(match: dict, projection: dict, db_collection: any, response_model: any):
    pipeline = [
              {
                  "$match": match
              },
              {
                  "$lookup": {
                      "from": "contract",
                       "let": { "solutionId": "$solution_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$solutionId"]
                                  }
                              }
                          }
                      ],
                      "as": "contract_field"
                  }
              },
              {
                  "$lookup": {
                      "from": "users",
                       "let": { "customerId": "$customer_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$customerId"]
                                  }
                              }
                          }
                      ],
                      "as": "customer_field"
                  }
              },
              {
                  "$unwind": "$contract_field"
              },
              {
                  "$unwind": "$customer_field"
              },
              {
                "$lookup": {
                    "from": "company",
                    "let": { "companyId": "$customer_field.company_id" },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": [ {"$toString": "$_id"}, "$$companyId"]
                                }
                            }
                        }
                    ],
                    "as": "company_field"
                  }
            },
            {
                "$unwind": "$company_field"
            },
            {
                  "$set": {
                      "sales_representative_nm": "$contract_field.sales_manager",
                      "customer_nm": "$customer_field.user_nm",
                      "company_id": "$customer_field.company_id",
                      "company_nm": "$company_field.company_nm"
                  }
            },
              {
                  "$project": projection
              },
              {
                  "$limit": 1
              }
          ]
    result = db_collection.aggregate(pipeline)
    content=[]
    for item in result:
        item['_id'] = str(item['_id'])
        item['wr_date'] = str(item['wr_date'])
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content[0]
