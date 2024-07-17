import json
from db.context import work_request_collection
import pymongo
from db.context import Database
from datetime import datetime
from bson import ObjectId
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
        "file": file,
        "del_yn": "N"
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
    work_request_collection.update_one(filter, {"$set": req_data})
    work_request_collection.update_one(filter, {"$set":{"file": file}})

async def update_recovery_request_work(
        id: str
        ):
    filter = {"_id": id}
    work_request_collection.update_one(filter, {"$set":{"delYn": "Y"}})

async def get_request_work_list(page: int, user_id: str):
    size = 5
    skip = (page - 1) * size
    print(user_id)
    print(page)
    projection = {"_id": 1, "user_id": 1, "request_title": 1, "customer_nm": 1, "request_date":1}
    work_item = work_request_collection.find({"user_id": user_id}, projection).skip(skip).limit(size)
    # if work_item:
    #     work_item["_id"] = str(work_list["_id"])
    work_list = list(work_item)
    numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(work_list)]
    print(numbered_items)
    return numbered_items

async def get_request_work_dtl(request_id: str):
    print(request_id)
    work_item = work_request_collection.find_one(ObjectId(request_id))
    if work_item:
        work_item["_id"] = str(work_item["_id"])
    return work_item
