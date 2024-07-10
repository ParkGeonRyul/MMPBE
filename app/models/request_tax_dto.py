from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class RequestTaxDTO:
    def __init__(self, user_id, request_dt, request_content, status):
        self.user_id = user_id
        self.request_dt = request_dt
        self.request_content = request_content
        self.status = status