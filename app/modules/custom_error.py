from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

app = FastAPI()

class testId(Exception):
    def __init__(self, test: str):
        self.test: str = test

@app.exception_handler(testId)
async def invalid_test_handler(request: Request, exc: testId):
    return JSONResponse(
        status_code=422,
        content={"message":"noooooo!"}
    )