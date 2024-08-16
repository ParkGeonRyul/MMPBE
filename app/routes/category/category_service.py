from fastapi import Request
from typing import List

import json

from db.context import user_collection, contract_collection

from models.work_request_dto import *
from models.category_dto import ResponseCategoryModel


async def get_category(request: Request) -> List[dict]:
    req_data = json.loads(await request.body())
    projection = { "_id": 1, "contract_title": 1, "company_id": 1, "inflow_path": 1, "sales_representative_nm": 1, "contract_date": 1}
    if req_data['role'] == 'user':
        get_user = user_collection.find_one({"_id": ObjectId(req_data['tokenData']['userId'])})
        dict_for_find = {"company_id": get_user['company_id']}
    
    elif req_data['role'] == 'admin' or req_data['role'] == 'system admin':
        dict_for_find = {"sales_representative_nm": req_data['tokenData']['name']}
        
    get_contract_by_user = contract_collection.find(dict_for_find, projection)
    content = []
    for item in get_contract_by_user:
        item['_id'] = str(item['_id'])
        model_instance = ResponseCategoryModel(**item)
        model_dict = model_instance.model_dump(by_alias=True, exclude_unset=True)
        content.append(model_dict)
        
    return content