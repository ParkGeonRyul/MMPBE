from fastapi import FastAPI

from utils import lifespan
from routes.auth import controller as auth_controller
from routes.page import controller as page_controller
from routes.user import controller as user_controller

from middlewares import cors_middleware
# from middlewares import static_middleware

from routes import index

app = FastAPI(lifespan=lifespan.lifespan)

cors_middleware.add(app)
# static_middleware.add(app)

app.include_router(auth_controller.router)
app.include_router(page_controller.router)
app.include_router(user_controller.router)