from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class ContractDTO:
    def __init__(
            self,
            contract_id,
            company_id,
            work_type,
            tenant_id, 
            inflow_path,
            customer_level,
            product_family,
            contract_amt,
            join_service,
            m_d,
            m_m,
            m_h,
            sales_manager,
            tech_manager,
            tax_mail,
            payment_standard,
            reg_dt,
            contract_dt,
            contracts_start_dt,
            contract_end_dt,
            last_modify_dt,
            del_yn
            ):
        self.contract_id = contract_id
        self.company_id = company_id
        self.work_type = work_type
        self.tenant_id = tenant_id
        self.inflow_path = inflow_path
        self.customer_level = customer_level
        self.product_family = product_family
        self.contract_amt = contract_amt
        self.join_service = join_service
        self.m_d = m_d
        self.m_m = m_m
        self.m_h = m_h
        self.sales_manager = sales_manager
        self.tech_manager = tech_manager
        self.tax_mail = tax_mail
        self.payment_standard = payment_standard
        self.reg_dt = reg_dt
        self.contract_dt = contract_dt
        self.contracts_start_dt = contracts_start_dt
        self.contract_end_dt = contract_end_dt
        self.last_modify_dt = last_modify_dt
        self.del_yn = del_yn