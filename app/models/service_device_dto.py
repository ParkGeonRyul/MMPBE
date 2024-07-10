from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class DeviceDTO:
    def __init__(
            self,
            company_nm,
            device_nm,
            device_type,
            public_ip,
            private_ip,
            created_at,
            updated_at,
            del_yn
            ):
        self.company_nm = company_nm
        self.device_nm = device_nm
        self.device_type = device_type
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.created_at = created_at
        self.updated_at = updated_at
        self.del_yn = del_yn