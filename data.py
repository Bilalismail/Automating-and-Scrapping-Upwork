from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    city: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class BasePay(BaseModel):
    amount: Optional[float] = None
    period: Optional[str] = None
    currency: Optional[str] = None

class PlatformIDs(BaseModel):
    employee_id: Optional[str] = None
    position_id: Optional[str] = None
    platform_user_id: Optional[str] = None

class Data(BaseModel):
    id: Optional[str] = None
    account: Optional[str] = None
    address: Optional[Address] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    picture_url: Optional[str] = None
    employment_status: Optional[str] = None
    employment_type: Optional[str] = None
    job_title: Optional[str] = None
    ssn: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    hire_date: Optional[str] = None
    termination_date: Optional[str] = None
    termination_reason: Optional[str] = None
    employer: Optional[str] = None
    base_pay: Optional[BasePay] = None
    pay_cycle: Optional[str] = None
    platform_ids: Optional[PlatformIDs] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Optional[dict] = None
