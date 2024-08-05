import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from utils import lifespan
from routes.auth import auth_controller
from routes.page import page_controller
from routes.user import user_controller
from routes.category import category_controller
from routes.request_work import request_work_controller
from routes.work_plan import work_plan_controllrer
from routes import index

from middlewares import cors_middleware
# from middlewares import static_middleware

app = FastAPI(lifespan=lifespan.lifespan)

cors_middleware.add(app)
# app.add_middleware(rbac.TokenVerifyMiddleware)
# static_middleware.add(app)

app.include_router(index.router)
app.include_router(auth_controller.router)
app.include_router(page_controller.router)
app.include_router(user_controller.router)
app.include_router(work_plan_controllrer.router)
app.include_router(request_work_controller.router)
app.include_router(category_controller.router)

@app.get("/ping")
def ping():
    return "pong"