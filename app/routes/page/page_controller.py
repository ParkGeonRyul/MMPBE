from datetime import datetime

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from db.context import Database


router = APIRouter(
    prefix="",
    tags=["Pages"],
    default_response_class=HTMLResponse
)

@router.get("/")
def main(req: Request):
    now = datetime.now()
    collection = Database.db.list_collection_names()
    print(f"Databases: {collection}")
    return "Hello,"
