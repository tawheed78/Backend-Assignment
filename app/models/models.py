from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Purchase(BaseModel):
    id: int
    user_id: int
    amount: float
    type: str
    installment_months: int

class PurchaseViaEMI(Purchase):
    emi_per_month: float
    

class PurchaseViaFixedInstallment(Purchase):
    fixed_amount_per_month: float
    
class User(BaseModel):
    user_id:str
    name :str
    email: str
    max_credit_limit: float
    available_limit: float
    purchases: List[PurchaseViaEMI]

class UserRegister(BaseModel):
    name:str
    email:str
    max_credit_limit: float

class Product(BaseModel):
    id: str
    name: str
    price: float

class Payment(BaseModel):
    id: str
    user_id: str
    amount: float
    payment_datetime: datetime 

class RepaymentPlan(BaseModel):
    user_id: int
    total_amount: float
    months: int
    monthly_payment: float
    interest_rate: float
