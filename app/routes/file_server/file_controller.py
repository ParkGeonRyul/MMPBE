from fastapi import APIRouter, HTTPException, status, Response, Request, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

import os
import uuid

from fastapi.responses import RedirectResponse
from routes.auth import auth_service
from constants import COOKIES_KEY_NAME
from dotenv import load_dotenv
from db.context import file_collection
from routes._path.api_paths import AUTH_CALLBACK, CHECK_SESSION, LOGIN_WITH_MS, LOGOUT, USER_INFO

load_dotenv()
router = APIRouter()

upload_path = os.getenv("UPLOAD_PATH")

@router.post("/test-upload")
async def test(file: UploadFile = File(None)):
    if file:
        test_uuid = str(uuid.uuid4())
        _, file_extension = os.path.splitext(file.filename)

        test_uuid_file = test_uuid + file_extension

        file_collection.insert_one({})

        upload_dir = upload_path
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, test_uuid_file)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        response_data = {"content": {"filename": file.filename}, "status_code": 200}

        return response_data
    
@router.get("/test-download")
async def test(uuid_filename:str):
    file_path = os.path.join(upload_path, uuid_filename)

    if not os.path.exists(file_path):
        return {"message": "File not found"}
    
    return FileResponse(path=file_path, filename=uuid_filename)