from pydantic import BaseModel, Field, ConfigDict, ValidationError
from utils.pymongo_object_id import PyObjectId

from pydantic.functional_validators import AfterValidator
from datetime import datetime
from typing import Any, List, Optional
from typing_extensions import Annotated
from bson import ObjectId
from pydantic.alias_generators import to_camel


class WorkPlanField:
    id = Field(
        description="ObjectID",
        alias="_id",
        default_factory=PyObjectId
    )
    user_id = Field(
        description="작업계획서 수신자 id(ObjectID)",
        alias="requester_id"
    )
    acceptor_id = Field(
        description="작업계획서 발신자 id(ObjectID)",
        min_length=1,
        default=None,
        alias="planId"
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
        default=None,
        alias="planDate"
    )
    file = Field(
        description="첨부 파일",
        example="Zone파일.zip",
        default=None,
        alias="file"
    )
    status = Field(
        description="승인 여부",
        example="요청, 회수, 승인, 반려",
        default=None,
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
        default=datetime.now(),
        alias="createdAt"
    )
    updated_at = Field(
        description="유저 정보 업데이트 된 마지막 날짜(UTC + 0)",
        default=datetime.now(),
        alias="updatedAt"
    )
    del_yn = Field(
        description="삭제된 여부",
        default="N",
        alias="delYn"
    )

class CreateWorkPlanModel(BaseModel): # fe -> be
    user_id: str = WorkPlanField.user_id #등록자 id (작업계획서 수신자 id)
    acceptor_id: str = WorkPlanField.acceptor_id # 발신자 id (작업요청자 수신자 id)
    request_id: str = WorkPlanField.request_id # 작업 요청서 id
    plan_title: str = WorkPlanField.plan_title # 필수
    plan_content: str = WorkPlanField.plan_content
    plan_date: Optional[datetime] = WorkPlanField.plan_date # None == 임시저장, 사용자가 요청 이후에 수정이 안 됨.
    file: Optional[str] = WorkPlanField.file #파일경로
    status: Optional[str] = WorkPlanField.status # 승인, 반려, 요청, 회수(시스템 관리자만 볼 수 있음)
    status_content : Optional[str] = WorkPlanField.status_content # 승인내용, 반려사유 (계획서 수신자가 작성)
    created_at: Optional[datetime] = WorkPlanField.created_at # 최초 이후 수정이 안 됨
    updated_at: Optional[datetime] = WorkPlanField.updated_at 
    del_yn: Optional[str] = WorkPlanField.del_yn # 시스템 관리자를 위한
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
        populate_by_name=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed = True,
        json_schema_extra={
            "example": {
                "userId": "6690cf7fa4897bf6b90541c1",
                "acceptorId": "작업요청자 수신자 id(ObjectID)",
                "requestId": "작업계획서(ObjectID)",
                "planTitle": "계획서 제목",
                "planContent": "계획서 내용",
                "planDate": "2024-08-05 00:00:00",
                "file": "파일 명",
                "status": "요청",
                "acceptorNm" : "제갈길동" ,
                "createdAt" : "2024-08-05 00:00:00",
                "updatedAt" : "2024-08-05 00:00:00",                
                "delYn": "N"
            }
        }
    )

class  UpdateWorkPlanModel(BaseModel):
    id: Optional[PyObjectId] = None
    user_id: Optional[str] = None
    device_nm: Optional[str] = None
    contact_nm: Optional[str] = None
    plan_title: Optional[str] = None
    customer_nm: Optional[str] = None
    plan_dt: Optional[datetime] = None
    plan_content: Optional[str] = None
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
                "status": "승인",
                "delYn": "삭제 여부"
            }
        }
    )

class  UpdatePlanStatusAcceptModel(BaseModel):
    status: Optional[str] = None
    statusContent: Optional[str] = None
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

# "_id": 1, "user_id": 1, "plan_title": 1, "acceptor_Id": 1, "acceptor_nm": 1, "plan_date": 1, "status": 1
class ResponsePlanListModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(alias="userId")
    plan_title: str = Field(alias="planTitle")
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
    requestor_nm: str = Field(alias="requestorNm")
    request_id: str = Field(alias="requestId")
    request_title: str = Field(alias="requestTitle")
    company_id: Optional[str] = Field(None, alias="companyId")
    company_nm: Optional[str] = Field(None, alias="companyNm")
    acceptor_id: str = Field(alias="acceptorId")
    acceptor_nm: Optional[str] = Field(None, alias="acceptorNm")
    plan_title: str = Field(alias='planTitle')
    plan_content: str = Field(alias='planContent')
    plan_date: datetime = Field(alias="planDate")
    file_path: str = Field(alias="filePath")
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

async def get_list(match: dict, projection: dict, db_collection: any, response_model: any):
    pipeline = [
                {
                    "$match": match
                },
                {
                  "$lookup": {
                        "from": "users",
                        "let": { "acceptorId": "$acceptor_id" },
                        "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$acceptorId"]
                                  }
                              }
                          }
                      ],
                      "as": "acceptor_field"
                  }
                },
                {
                  "$lookup": {
                      "from": "users",
                       "let": { "userId": "$user_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$userId"]
                                  }
                              }
                          }
                      ],
                      "as": "user_field"
                  }
                },
                {
                    "$unwind": {
                        "path": "$acceptor_field",
                        "preserveNullAndEmptyArrays": True
                        }
                },
                {
                    "$unwind": {
                        "path": "$user_field",
                        "preserveNullAndEmptyArrays": True
                        }
                },
                {
                    "$set": {
                        "acceptor_id": {"$toString": "$acceptor_field._id"},
                        "acceptor_nm": "$acceptor_field.user_nm",
                        "requestor_nm": "$user_field.user_nm"
                    }
                },
                {
                  "$lookup": {
                        "from": "company",
                        "let": { "companyId": "$acceptor_field.company_id" },
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
                    "$unwind": {
                        "path": "$company_field",
                        "preserveNullAndEmptyArrays": True
                        }
                },
                {
                    "$set": {
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
        if match['plan_date'] == {'$ne': None}:
            item['plan_date'] = item['plan_date'].strftime('%Y-%m-%d')
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)

    return content

async def get_dtl(match: dict, projection: dict, db_collection: any, response_model: any):
    pipeline = [
              {
                  "$match": match
              },
              {
                  "$lookup": {
                      "from": "users",
                       "let": { "acceptorId": "$acceptor_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$acceptorId"]
                                  }
                              }
                          }
                      ],
                      "as": "acceptor_field"
                  }
              },
              {
                  "$lookup": {
                      "from": "users",
                       "let": { "userId": "$user_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$userId"]
                                  }
                              }
                          }
                      ],
                      "as": "user_field"
                  }
              },
              {
                  "$lookup": {
                      "from": "workRequest",
                       "let": { "requestId": "$request_id" },
                      "pipeline": [
                          {
                              "$match": {
                                  "$expr": {
                                      "$eq": [ {"$toString": "$_id"}, "$$requestId"]
                                  }
                              }
                          }
                      ],
                      "as": "request_field"
                  }
              },
              {
                  "$unwind": "$acceptor_field"
              },
              {
                  "$unwind": "$user_field"
              },
              {
                  "$unwind": "$request_field"
              },
              {
                "$lookup": {
                    "from": "company",
                    "let": { "companyId": "$acceptor_field.company_id" },
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
                      "requestor_nm": "$user_field.user_nm",
                      "request_title": "$request_field.wr_title",
                      "company_id": "$acceptor_field.company_id",
                      "company_nm": "$company_field.company_nm",
                      "customer_nm": "$customer_field.user_nm",
                      "acceptor_nm": "$acceptor_field.user_nm",
                      "company_nm": "$company_field.company_nm",
                      "file_path": "file"
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
        item['plan_date'] = str(item['plan_date'])
        model_instance = response_model(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
        # content.append(item)

    return content[0]