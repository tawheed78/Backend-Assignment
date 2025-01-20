from models.models import PurchaseViaEMI, PurchaseViaFixedInstallment

class User:
    def __init__(self, user_id, name, email, max_credit_limit):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.max_credit_limit = max_credit_limit
        self.available_limit = max_credit_limit
        self.purchases = {}

class UserManager:
    def __init__(self):
        self.users = {}
        self.user_count = 1
        self.purchase_count = 1

    def register_user(self, name, email, max_credit_limit):
        user_id = self.user_count
        self.user_count += 1
        new_user = User(user_id, name, email,max_credit_limit)
        self.users[user_id] = new_user
        return new_user
    

    def make_purchase_via_emi(self, user_id, amount, emi_per_month, total_months):
        user = self.users.get(user_id)
        purchase = PurchaseViaEMI(
            id=self.generate_id(),
            user_id=user_id,
            amount=amount,
            emi_per_month=emi_per_month,
            installment_months=total_months,
            type= 'EMI'
        )
        return purchase
    
    def make_purchase_via_fixed_installemnt(self, user_id, amount, fixed_amount_per_month, installment_months):
        user = self.users.get(user_id)
        purchase = PurchaseViaFixedInstallment(
            id = self.generate_id(),
            user_id = user_id, 
            amount= amount, 
            fixed_amount_per_month=fixed_amount_per_month,
            installment_months = installment_months,
            type= 'FIXED')
        return purchase
        
    def get_available_limit(self, user_id:int):
        user = self.users.get(user_id)
        return user.available_limit
    
    def make_payment(self, user_id, amount):
        user = self.users.get(user_id)
        user.available_limit += amount
    
    def generate_id(self):
        pid = self.purchase_count
        self.purchase_count += 1
        return int(pid)
