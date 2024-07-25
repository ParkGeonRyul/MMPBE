import pymongo
from db.context import *

class test:
    test= "test"

class NotNull:
      not_null = {'$ne': None}

async def get_collection_list(user_id: str, db_collection: str, is_null: dict | None, page: int, projection: dict):
        skip = (page - 1) * 5
        work_total = db_collection.count_documents({"user_id": user_id, "created_at": is_null})
        work_item = db_collection.find({"user_id": user_id, "created_at":  is_null}, projection).skip(skip).limit(5)
        work_list = list(work_item)
        numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(work_list)]

        content = {
            "total": work_total,
            "work_list": numbered_items
        }

        return content
