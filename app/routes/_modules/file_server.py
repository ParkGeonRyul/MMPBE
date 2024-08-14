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

async def download_file(file_id:str | None):
    if file_id:
        test = file_collection.find_one({"_id": ObjectId(file_id)})
        uuid_filename = test['uuid']
        file_path = os.path.join(upload_path, uuid_filename)

        if not os.path.exists(file_path):
            return {"message": "File not found"}
        
        return file_path
    
    return None

async def generate_multipart_response(item, file_path):
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }

    async def response_generator():
        # JSON part
        json_part = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"json_data\"\r\n"
            f"Content-Type: application/json\r\n\r\n"
            f"{jsonable_encoder(item)}\r\n"
        )
        yield json_part.encode("utf-8") 

        if file_path:
            # File part
            file_part_header = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(file_path)}\"\r\n"
                f"Content-Type: application/octet-stream\r\n\r\n"
            )
            yield file_part_header.encode("utf-8")
            
            async with aiofiles.open(file_path, 'rb') as file:
                chunk = await file.read(1024)
                while chunk:
                    yield chunk
                    chunk = await file.read(1024)

            # Closing boundary
            yield f"\r\n--{boundary}--\r\n".encode("utf-8")

    return StreamingResponse(response_generator(), headers=headers)