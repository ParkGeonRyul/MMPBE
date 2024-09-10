import os
import sys
import json

from fastapi.responses import JSONResponse

from utils.logger_handler import exception_log_callback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Request
from utils import lifespan
from routes.auth import auth_controller
from routes.page import page_controller
from routes.customer import customer_controller
from routes.category import category_controller
from routes.work_plan import work_plan_controllrer
from routes.work_request import work_request_controller
from routes import bi_embeded
from routes import index

from middlewares import cors_middleware
# from middlewares import static_middleware

app = FastAPI(lifespan=lifespan.lifespan)

cors_middleware.add(app)
# app.add_middleware(rbac.TokenVerifyMiddleware)
# static_middleware.add(app)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    await exception_log_callback(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
app.include_router(index.router)
app.include_router(auth_controller.router)
app.include_router(page_controller.router)
app.include_router(customer_controller.router)
app.include_router(work_plan_controllrer.router)
app.include_router(work_request_controller.router)
app.include_router(category_controller.router)
app.include_router(bi_embeded.router)

@app.get("/ping")
def ping():
    return "pong"