from db.context import *
from models import *

class test:
    test= "test"

async def is_temporary(value: bool):
      if value == True:
        return None
      else: 
        return {'$ne': None}

async def get_collection_list(match: dict, db_collection: str, projection: dict, response_model: any, dto: any) -> list: # page: int | None
  get_list: list = await dto.get_list(match, projection, db_collection, response_model)

  return get_list

async def get_collection_dtl(match: dict, db_collection: str, projection: dict, response_model: any, dto: any):
  get_dtl = await dto.get_dtl(match, projection, db_collection, response_model)

  return get_dtl