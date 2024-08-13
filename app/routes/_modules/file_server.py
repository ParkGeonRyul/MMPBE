from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import uuid

import os

from db.context import file_collection


load_dotenv()

upload_path = os.getenv("UPLOAD_PATH")

async def upload_file(file: UploadFile = File(None)):
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

async def download_file(uuid_filename:str):
    file_path = os.path.join(upload_path, uuid_filename)

    if not os.path.exists(file_path):
        return {"message": "File not found"}
    
    return FileResponse(path=file_path, filename=uuid_filename)