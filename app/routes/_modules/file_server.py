from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from bson import ObjectId

import uuid
import os
import aiofiles

from db.context import file_collection


load_dotenv()

upload_path = os.getenv("UPLOAD_PATH")

async def upload_file(id: str, file: UploadFile = File(...)):
    uuid_data = str(uuid.uuid4())
    _, file_extension = os.path.splitext(file.filename)

    uuid_file = uuid_data + file_extension

    upload_dir = upload_path + "/" + id
    if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, uuid_file)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    type = file_extension.split('.')

    file_data = {
        'origin': file.filename,
        'uuid': uuid_file,
        'extension': type[1],
        'size': file.size,
        'user_id': id
        }
    insert_file_data = file_collection.insert_one(file_data)
    response_data = {"file_id": str(insert_file_data.inserted_id)}

    return response_data

async def download_file(file_id:str | None):
    if file_id:
        test = file_collection.find_one({"_id": ObjectId(file_id)})
        uuid_filename = test['uuid']
        file_path = os.path.join(upload_path, uuid_filename)

        if not os.path.exists(file_path):
            return {"message": "File not found"}
        
        return file_path
    
    return None
