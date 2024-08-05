import pymongo
from db.context import *

class test:
    test= "test"

async def is_temprary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(user_id: str, db_collection: str, is_null: dict | None, page: int | None, projection: dict):
        skip = (page - 1) * 5
        db_total = db_collection.count_documents({"user_id": user_id, "created_at": is_null})
        db_item = db_collection.find({"user_id": user_id, "created_at":  is_null}, projection).skip(skip).limit(5)
        db_list = list(db_item)
        numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(db_list)]

        content = {
            "total": db_total,
            "work_list": numbered_items
        }

        return content
