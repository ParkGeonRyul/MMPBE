from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class TaxDTO:
    def __init__(self, user_id, tax_id, tax_money, tax_dt):
        self.user_id = user_id
        self.tax_id = tax_id
        self.tax_money = tax_money
        self.tax_dt = tax_dt