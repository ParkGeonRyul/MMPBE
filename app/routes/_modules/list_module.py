from db.context import *
from models import *

class test:
    test= "test"

async def is_temporary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(match: dict, projection: dict, response_model: any, dto: any, skip: int, limit: int) -> list: # page: int | None
  get_list = await dto.get_list(match, projection, response_model, skip, limit)

  return get_list

async def get_collection_dtl(match: dict, db_collection: str, projection: dict, response_model: any, dto: any):
  get_dtl = await dto.get_dtl(match, projection, db_collection, response_model)

  return get_dtl