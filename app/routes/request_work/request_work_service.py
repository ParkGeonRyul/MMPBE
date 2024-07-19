import json
from db.context import workRequestCollection
import pymongo
from db.context import Database
from datetime import datetime

from utils import objectCleaner


async def post_request_work(
        user_id: str,
        device_nm: str,
        request_title: str,
        customer_nm: str,
        request_date: str,
        work_content: str,
        file: str
        ):
    document = {
        "user_id": user_id,
        "device_nm": device_nm,
        "request_title": request_title,
        "customer_nm": customer_nm,
        "request_date": request_date,
        "work_content": work_content,
        "file":file
    }
    workRequestCollection.insert_one(document)

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
    workRequestCollection.update_one(filter, {"$set": req_data})
    workRequestCollection.update_one(filter, {"$set":{"file": file}})

async def update_recovery_request_work(
        id: str
        ):
    filter = {"_id": id}
    workRequestCollection.update_one(filter, {"$set":{"delYn": "Y"}})

async def get_request_work_list(page: int, token: str):
    size = 5

    projection = {"_id": 1, "user_id": 1, "request_itle": 1, "customer_nm": 1, "request_date":1}
    work_item = workRequestCollection.find({"userId": user_id}, projection).skip(page).limit(size)
    work_list = list(work_item)
    return work_list

async def get_request_work_dtl(request_id: str, token: str):
    work_item = workRequestCollection.find_one({"request_id":request_id})
    return work_item