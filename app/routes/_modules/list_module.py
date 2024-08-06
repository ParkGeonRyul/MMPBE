import pymongo
from db.context import *

class test:
    test= "test"

async def is_temprary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(user_id: str, db_collection: str, is_null: str | None, page: int | None, projection: dict, response_model: any):
        skip = (page - 1) * 5
        db_total = db_collection.count_documents({"user_id": user_id, "request_date": is_null})
        db_item = db_collection.find({"user_id": user_id, "request_date":  is_null}, projection).skip(skip).limit(5)
        content=[]
        for item in db_item:
            item['_id'] = str(item['_id'])
            item['created_at'] = item['created_at'].isoformat()
            model_instance = response_model(**item)
            model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
            content.append(model_dict)
        numbered_items = [{"number": skip + i + 1, **item, "_id": str(item["_id"])} for i, item in enumerate(content)]

        response = {
            "total": db_total,
            "work_list": numbered_items
        }

        return response
