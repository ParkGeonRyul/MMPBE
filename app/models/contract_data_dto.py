from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class ContractDataDTO:
    def __init__(self, contract_id, user_id, title, content, file, contract_dt, approval_yn, created_at, updated_at, del_yn):
        self.contract_id = contract_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.file = file
        self.contract_dt = contract_dt
        self.approval_yn = approval_yn
        self.created_at = created_at
        self.updated_at = updated_at
        self.del_yn = del_yn