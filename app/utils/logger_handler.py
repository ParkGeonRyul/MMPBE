import logging

# 커스텀 핸들러
class DBHandler(logging.Handler):
    def __init__(self, db_session: AsyncSession):
        logging.Handler.__init__(self)
        self.db_controller = MongoController() 

    def emit(self, record): 
        # 이게 헨들러가 시작될 때 오는 것 같아요
        # Log 기록할 때 Thread로 하고 (DB 저장할 때만)
        # Local일 때는 print log, Server일 때는 DB Log 저장
        log_entry = Log(level=record.levelname, message=record.msg) # 이건 로그 포멧

    def record_db(self, record):
        """

        :param record:

        """
        data = dict(record.__dict__)
        data["server"] = Config().get_env("SERVER_TYPE")
        # Remove non-serializable types or convert them to string
        for key, value in data.items():
            if isinstance(value, Exception):
                data[key] = str(value)
        self.db_controller.insert_one("log", data)

def setup_logger():
    # 여기에 DBHandler 추가하고 다른 파일에서 사용
    """ """
    logger = logging.getLogger("slack_logger")
    