import json
from db.context import work_request_collection
import pymongo
from db.context import Database
from datetime import datetime

from utils import objectCleaner


async def postRequestWork(
        userId: str,
        deviceNm: str,
        requestTitle: str,
        customerNm: str,
        requestDt: str,
        workContent: str,
        file: str,
        delYn: str
        ):
    document = {
        "userId": userId,
        "deviceNm": deviceNm,
        "requestTitle": requestTitle,
        "customerNm": customerNm,
        "requestDt": requestDt,
        "workContent": workContent,
        "file":file,
        "delYn":delYn
    }
    work_request_collection.insert_one(document)

async def updateModifyRequestWork(
        id: str,
        userId: str,
        deviceNm: str,
        requestTitle: str,
        customerNm: str,
        requestDt: str,
        workContent: str,
        file: str
        ):
    filter = {"_id": id}
    reqData = objectCleaner.cleanObject({
        "userId": userId,
        "deviceNm": deviceNm,
        "requestTitle": requestTitle,
        "customerNm": customerNm,
        "requestDt": requestDt,
        "workContent": workContent
        })
    work_request_collection.update_one(filter, {"$set": reqData})
    work_request_collection.update_one(filter, {"$set":{"file": file}})

async def updateRecoveryRequestWork(
        id: str
        ):
    filter = {"_id": id}
    work_request_collection.update_one(filter, {"$set":{"delYn": "Y"}})

    return "success"

async def testDrive(item:dict):
    return item
