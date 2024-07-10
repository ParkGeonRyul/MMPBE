from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class RoleDTO:
    def __init__(self, role_id, role_nm):
        self.role_id = role_id
        self.role_nm = role_nm