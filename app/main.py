from fastapi import FastAPI

from utils import lifespan
from controllers import auth_controller
from controllers import page_controller
from controllers import user_controller

from middlewares import cors_middleware
# from middlewares import static_middleware

from models.user_dto import UserModel


# app = FastAPI()
app = FastAPI(lifespan=lifespan.lifespan)

cors_middleware.add(app)
# static_middleware.add(app)

app.include_router(auth_controller.router)
app.include_router(page_controller.router)
app.include_router(user_controller.router)

@app.post("/test", status_code=200)
async def create_item(item: UserModel):
    return item