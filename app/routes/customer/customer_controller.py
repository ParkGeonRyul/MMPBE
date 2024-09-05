from fastapi import APIRouter, Request

from routes._path.api_paths import SELECT_CUSTOMER, SELECT_CUSTOMER_DETAIL
from routes.customer import customer_service


router = APIRouter()

@router.get(SELECT_CUSTOMER)
async def get_customer():
    return await customer_service.get_customer_list()

@router.get(SELECT_CUSTOMER_DETAIL)
async def get_customer(request: Request):
    return await customer_service.get_customer_detail(request)