import json
from db.context import work_request_collection
import pymongo
from db.context import Database
from datetime import datetime
from bson import ObjectId
from utils import objectCleaner

from utils import objectCleaner


async def postRequestWork(
        userId: str,
        deviceNm: str,
        requestTitle: str,
        customerNm: str,
        requestDt: str,
        workContent: str,
        file: str
        ):
    document = {
        "userId": userId,
        "deviceNm": deviceNm,
        "requestTitle": requestTitle,
        "customerNm": customerNm,
        "requestDt": requestDt,
        "workContent": workContent,
        "file":file
    }
    work_request_collection.insert_one(document)

async def update_modify_request_work(
        id: str,
        user_id: str,
        device_nm: str,
        request_title: str,
        customer_nm: str,
        request_date: str,
        work_content: str,
        file: str,
        del_yn: str
        ):
    filter = {"_id": id}
    req_data = objectCleaner.cleanObject({
        "user_id": user_id,
        "device_nm": device_nm,
        "request_title": request_title,
        "customer_nm": customer_nm,
        "request_date": request_date,
        "work_content": work_content,
        "del_yn": del_yn
        })
    workRequestCollection.update_one(filter, {"$set": reqData})
    workRequestCollection.update_one(filter,{"$set":{"file":file}})