import logging

from fastapi import HTTPException, Request, logger
from fastapi.responses import JSONResponse

# from app.config import Config
from models.login_log_dto import LoginLogModel
from models.work_log_dto import WorkLogModel
from db.context import login_log_collection
from db.context import work_log_collection



async def login_log_callback(log_in_out : str,user_email : str,success_YN : str, client_ip: str, user_agent:str):
    log_dic = {
        "log_in_out" : log_in_out,
        "user_email" : user_email,
        "user_agent" : user_agent,
        "success_YN" : success_YN,
        "client_ip" : client_ip,
    }
    log_document = dict(LoginLogModel(**log_dic))
    login_log_collection.insert_one(log_document)

async def work_log_callback(path : str, method : str, client_ip : str, user_agent : str, userId : str):
    
    log_dic = {
        "path" : path,
        "method" : method,
        "user_agent" : user_agent,
        "client_ip" : client_ip,
        "user_id" : userId,
        "exception_result" :None
    }
    log_document = dict(WorkLogModel(**log_dic))
    result = work_log_collection.insert_one(log_document)
    print("work_log_callback result ::: ", result)
    
# 커스텀 핸들러
class DBHandler(logging.Handler):
    print("로깅로깅로깅 logging.Handler ::::", logging.Handler)
    def __init__(self):
        logging.Handler.__init__(self)
        # self.db_controller = MongoController() 

    # def emit(self, record): 
    #     # 이게 헨들러가 시작될 때 오는 것 같아요
    #     # Log 기록할 때 Thread로 하고 (DB 저장할 때만)
    #     # Local일 때는 print log, Server일 때는 DB Log 저장
    #     log_entry = Log(level=record.levelname, message=record.msg) # 이건 로그 포멧

    def record_db(self, record):
        print("로깅로깅로깅 record :::: ", record)
        print("로깅로깅로깅 self :::: ", self)
        """

        :param record:

        """
        # data = dict(record.__dict__)
        # data["server"] = Config().get_env("SERVER_TYPE")
        # # Remove non-serializable types or convert them to string
        # for key, value in data.items():
        #     if isinstance(value, Exception):
        #         data[key] = str(value)
        # self.db_controller.insert_one("log", data)

# def setup_logger():
#     # 여기에 DBHandler 추가하고 다른 파일에서 사용
#     """ """
#     logger = logging.getLogger("db_logger")


# 예외 처리기 (Exception이 호출될 때 Intercept)
# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request: Request, exc: HTTPException):
#     async for db in get_db():
#         # 커스텀 핸들러를 로거에 추가
        
#         handler = DBHandler(db)
#         logger.addHandler(handler)
        
#         # 예외 발생 시 로거에 로그 기록
#         logger.error(f"HTTP Exception: {exc.detail}")
        
#         # 커스텀 응답 반환
#         return JSONResponse(
#             status_code=exc.status_code,
#             content={"message": f"Custom Exception: {exc.detail}"}
#         )
