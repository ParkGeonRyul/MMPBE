from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class ServiceUsageDTO:
    def __init__(
            self,
            user_id,
            cpu_usage,
            disk_usage,
            service_device_id
            ):
        self.user_id = user_id
        self.cpu_usage = cpu_usage
        self.disk_usage = disk_usage
        self.service_device_id = service_device_id