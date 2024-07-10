from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class CompanyDTO:
    def __init__(self, company_id, company_name):
        self.company_id = company_id
        self.company_name = company_name