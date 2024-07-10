from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class RequestDTO:
    def __init__(
            self,
            request_id,
            user_id,
            company_nm,
            device_nm,
            contact_nm,
            request_title,
            customer_nm,
            request_dt,
            work_content,
            file,
            approval_yn,
            status_yn,
            acceptor_nm,
            request_status,
            created_at,
            updated_at,
            del_yn
            ):
        self.request_id = request_id
        self.user_id = user_id
        self.company_nm = company_nm
        self.device_nm = device_nm
        self.contact_nm = contact_nm
        self.request_title = request_title
        self.customer_nm = customer_nm
        self.request_dt = request_dt
        self.work_content = work_content
        self.file = file
        self.approval_yn = approval_yn
        self.status_yn = status_yn
        self.acceptor_nm = acceptor_nm
        self.request_status = request_status
        self.created_at = created_at
        self.updated_at = updated_at
        self.del_yn = del_yn