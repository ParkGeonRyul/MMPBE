from fastapi import FastAPI

from utils import lifespan
from app.controllers import auth_controller
from app.controllers import page_controller
from app.controllers import user_controller

from app.middlewares import cors_middleware
# from middlewares import static_middleware


app = FastAPI(lifespan=lifespan.lifespan)

cors_middleware.add(app)
# static_middleware.add(app)