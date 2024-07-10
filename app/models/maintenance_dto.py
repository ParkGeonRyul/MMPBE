from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class MaintenanceDTO:
    def __init__(
            self,
            maintenance_id,
            user_id,
            title,
            content,
            file,
            maintenance_dt,
            approval_yn,
            status,
            created_at,
            updated_at,
            del_yn
            ):
        self.maintenance_id = maintenance_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.file = file
        self.maintenance_dt = maintenance_dt
        self.approval_yn = approval_yn
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.del_yn = del_yn