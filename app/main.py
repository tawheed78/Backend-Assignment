from fastapi import FastAPI, HTTPException

from fastapi.responses import JSONResponse
from services.user_service import UserManager
from models.models import UserRegister, Purchase

app = FastAPI()

purchase_db = {}

user_manager = UserManager()
user_db = user_manager.users

def calculate_emi(amount, months):
    emi_per_month = (amount + (amount*0.8))/months
    return emi_per_month

def calculate_fixed(amount, months):
    fixed_per_month = (amount/months)
    return fixed_per_month

@app.post("/register")
def register_user(user: UserRegister):
    user = user_manager.register_user(user.name, user.email,user.max_credit_limit)
    user_db[user.user_id] = user
    return user

@app.get("/user/limit")
def user_limit(user_id:int):
    return user_manager.get_available_limit(user_id)

@app.post("/purchase/")
def make_purchase(purchase: Purchase):
    if purchase.user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found.")
    user_id = purchase.user_id
    user = user_db.get(user_id)
    user_available_limit = user_manager.get_available_limit(user_id)
    if user_available_limit < purchase.amount:
        raise HTTPException(status_code=40, detail="Insufficient credit limit")
    user_available_limit -= purchase.amount
    if purchase.type == 'EMI':
        emi_amount = calculate_emi(purchase.amount, purchase.installment_months)
        response = user_manager.make_purchase_via_emi(user_id, purchase.amount, emi_amount,purchase.installment_months)
        purchase_db[response.id] = response
        return response
    elif purchase.type == "FIXED":
        fixed_amount = calculate_fixed(purchase.amount, purchase.installment_months)
        response = user_manager.make_purchase_via_fixed_installemnt(user_id, purchase.amount, fixed_amount, purchase.installment_months)
        purchase_db[response.id] = response
        return response
    
@app.post("/pay/")
def pay_amount(pid:int,user_id:int, amount:float):
    if pid not in purchase_db:
        raise HTTPException(status_code=404, detail="PID not found.")
    payment = purchase_db.get(pid)
    response = user_manager.make_payment(user_id,amount)
    return JSONResponse(f"EMI received against purchase ID: {pid}")

@app.get("/user/puchases/")
def get_user_purchases(user_id:int):
    if not user_id in user_db:
        raise HTTPException(status_code=404, detail="User not found.") 
    user = user_db.get(user_id)
    return user.purchases