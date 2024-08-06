from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic.alias_generators import to_camel
from db.context import work_request_collection
from motor.motor_asyncio import AsyncIOMotorClient

import motor.motor_asyncio

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
    request_title = Field(
        description="작업 요청 제목",
        example="Web DNS 설정",
        min_length=1,
        alias="requestTitle"
    )
    request_content = Field(
        description="작업 요청 내용",
        example="Web DNS 설정 및....",
        min_length=1,
        alias="requestContent"
    )
    request_date = Field(
        description="요청 일자(UTC + 0), 임시저장 일때는 NULL",
        default=None,
        alias="requestDate"
    )
    file = Field(
        description="파일 경로",
        default=None
    )
    status = Field(
        description="요청 상태",
        examples="요청, 회수, 승인, 반려",
        default="요청"
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
    request_title: str = WorkRequestField.request_title # 필수
    request_content: str = WorkRequestField.request_content
    request_date: Optional[datetime] = WorkRequestField.request_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    file: str = WorkRequestField.file
    status: Optional[str] = WorkRequestField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
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
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "delYn": "삭제 여부"
            }
        }
    )

class  UpdateWorkRequestModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    device_nm: Optional[str] = None
    contact_nm: Optional[str] = None
    request_title: Optional[str] = None
    customer_nm: Optional[str] = None
    request_dt: Optional[datetime] = None
    work_content: Optional[str] = None
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
                "requestTitle": "요청 제목",
                "customerNm": "고객 이름",
                "requestDate": "임시저장 == NULL",
                "content": "작업 내용",
                "file": "파일 명",
                "status": "승인, 반려, 요청, 회수",
                "delYn": "삭제 여부"
            }
        }
    )

class DeleteRequestTempraryModel(BaseModel):
    ids: List[str]

class ResponseRequestListModel(BaseModel):
    id: str = Field(alias="_id")
    request_title: str = Field(alias="requestTitle")
    sales_representative_nm: str = Field(alias="salesRepresentativeNm")
    request_date: Optional[str] = Field(None, alias="requestDate")
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
                "requestDate": "임시저장 == NULL",
                "status": "승인, 반려, 요청, 회수"
            }
        }
    )

async def get_list(id: str, projection: dict, is_null: str | None, db_collection: any, skip: int, response_model: any):
    pipeline = [
              {
                  "$match": {
                      "customer_id": id,
                      "request_date": is_null
                  }
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
                  "$unwind": "$contract_field"
              },
              {
                  "$set": {
                      "sales_representative_nm": "$contract_field.sales_manager"
                  }
              },
              {
                  "$project": projection
              },
              {
                  "$skip": skip
              },
              {
                  "$limit": 5
              }
          ]
    results = db_collection.aggregate(pipeline)
    content=[]
    for item in results:
        item['_id'] = str(item['_id'])
        if is_null == {'$ne': None}:
            item['request_date'] = item['request_date'].strftime('%Y-%m-%d')
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
    numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(content)]

    return numbered_items


    # Request Work Dtl
    # rwId: string; // _id
    # companyId: string;
    # customerNm: string;
    # customerId: string
    # content: string;
    # rwDate: IDateValue
    # filePath: string;
    # status: "승인" | "반려" | "요청" | "회수";
    # statusContent: string;