from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import uuid

import os

from db.context import file_collection


load_dotenv()

upload_path = os.getenv("UPLOAD_PATH")

async def upload_file(file: UploadFile = File(...)):
    uuid_data = str(uuid.uuid4())
    _, file_extension = os.path.splitext(file.filename)

    uuid_file = uuid_data + file_extension

    upload_dir = upload_path
    if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, uuid_file)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    file_data = {
        'origin': file.filename,
        'uuid': uuid_file,
        'extension': file_extension,
        'size': file.size
        }
    insert_file_data = file_collection.insert_one(file_data)
    response_data = {"file_id": str(insert_file_data.inserted_id)}

    return response_data

async def download_file(uuid_filename:str):
    file_path = os.path.join(upload_path, uuid_filename)

    if not os.path.exists(file_path):
        return {"message": "File not found"}
    
    return FileResponse(path=file_path, filename=uuid_filename)