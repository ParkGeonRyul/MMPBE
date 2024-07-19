import json
from db.context import work_request_collection
import pymongo
from db.context import Database


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
    workRequestCollection.insert_one(document)

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
    workRequestCollection.update_one(filter, {"$set": reqData})
    workRequestCollection.update_one(filter, {"$set":{"file": file}})

async def updateRecoveryRequestWork(
        id: str
        ):
    filter = {"_id": id}
    workRequestCollection.update_one(filter, {"$set":{"delYn": "Y"}})

    return "success"