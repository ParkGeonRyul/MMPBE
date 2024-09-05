from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from db.context import auth_collection


scheduler = BackgroundScheduler()

def auth_initialize():
    auth_collection.delete_many({})
auth_trigger = CronTrigger(hour=3, minute=0, second=0, timezone='Asia/Seoul')
scheduler.add_job(auth_initialize, auth_trigger)

@asynccontextmanager
async def lifespan(app: FastAPI):

    # 서버 시작 시 실행할 작업
    scheduler.start()
    yield

    # 서버 종료 시 실행할 작업
    scheduler.shutdown()