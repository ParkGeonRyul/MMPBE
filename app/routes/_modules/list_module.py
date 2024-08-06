import pymongo
from db.context import *
from models import *

class test:
    test= "test"

async def is_temprary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(id: str, db_collection: str, is_null: str | None, page: int | None, projection: dict, response_model: any, dto: any):
        skip = (page - 1) * 5
        db_total = db_collection.count_documents({"customer_id": id, "request_date": is_null})
        get_list = await dto.get_list(id, projection, is_null, db_collection, skip, response_model)
        content = {
            "total": db_total,
            "list": get_list
        }
        return content