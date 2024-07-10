from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class UserDTO:
    def __init__(
            self,
            user_id,
            company_id,
            user_email,
            user_nm,
            rank,
            company_contact,
            mobile_contact,
            email,
            responsible_party,
            role,
            created_at,
            updated_at,
            del_yn
            ):
        self.user_id = user_id
        self.company_id = company_id
        self.user_email = user_email
        self.user_nm = user_nm
        self.rank = rank
        self.company_contact = company_contact
        self.mobile_contact = mobile_contact
        self.email = email
        self.responsible_party = responsible_party
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.del_yn = del_yn
        self.del_yn = del_yn