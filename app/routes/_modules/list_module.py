import pymongo
from db.context import *
from models import *

class test:
    test= "test"

async def is_temporary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(match: dict, db_collection: str, projection: dict, response_model: any, dto: any): # page: int | None, match: dict, 
        # skip = (page - 1) * 5
        db_total = db_collection.count_documents(match)
        get_list = await dto.get_list(match, projection, db_collection, response_model)
        content = {
            "total": db_total,
            "list": get_list
        }
        return content

async def get_collection_dtl(id: str, db_collection: str, is_temporary: str | None, projection: dict, response_model: any, dto: any):
    get_dtl = await dto.get_dtl(id, projection, is_temporary, db_collection, response_model)

    return get_dtl