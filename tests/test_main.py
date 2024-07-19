from fastapi.testclient import TestClient

from app.main import app
from app.db.context import Database
from app.db.context import workRequestCollection

import pymongo
import pytest
from httpx import AsyncClient, ASGITransport

client = TestClient(app)

# cors_middleware.add(app)
# static_middleware.add(app)

@pytest.mark.anyio
async def testCode_postWork():
    document = {
        "userId": "6690cf7fa4897bf6b90541c1",
        "deviceNm": "test",
        "requestTitle": "test",
        "customerNm": "test",
        "requestDt": "2024-07-19",
        "workContent": "test"
    }
    response = client.post("/request-work", json=document)
    
    if response.status_code == 201:
        filter_query = {"userId": document.get('userId')}
        workRequestCollection.delete_one(filter_query)
        return True
    else:
        return False
    
@pytest.mark.anyio
async def testCode_putWork():
    document = {
        "id":"6699f50f39111c39d9792ef7",
        "userId": "6690cf7fa4997bf6ba0546c2",
        "deviceNm": "tesststststt"
    }
    response = client.post("/request-work", json=document)
    
    if response.status_code == 200:
        return True
    else:
        return False