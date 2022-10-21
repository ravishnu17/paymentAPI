from pydantic import BaseModel , EmailStr

class Transaction_info(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    paid_to:str
    transaction_id:str
    refund_link:str
    amount:float
    
    class Config:
        orm_model = True