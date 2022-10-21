from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
import requests
from Configurations.config import secret
from DBConnection.dbConnection import get_db
from Schemas.Schema import Transaction_info
from Model.model_payment import PaymentData


root = APIRouter(
    tags=["Payment"]
)
invoice = 97700878357

def getLink(data,token):
    
    #payments data
    # total = int(data['price'])*int(data['quantity'])
    global payment_header , execute_url
    
    payment_url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
    payment_header = {"Authorization" : f"{token['token_type']} {token['access_token']}"}
    payment_data = {
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"
    },
    "transactions": [{
        "amount": {
        "total":int(data['amount'])+0.07 ,
        "currency": "USD",
        "details": {
            "subtotal": data['amount'],
            "tax": "0.07"
        }
        },
        "description": "Donate to the people.",
        "invoice_number": data['invoice'],
        "payment_options": {
        "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
        },
        "soft_descriptor": "ECHI5786786",
        # "item_list": {
        # "items": [{
        #     "name": "Ticket",
        #     "description": "Event name",
        #     "quantity": data['quantity'],
        #     "price": data['price'],
        #     "currency": "USD"
        # }],

        # }
    }],
    
    "note_to_payer": "Contact us for any questions on your order.",
    "redirect_urls": {
        "return_url": "http://localhost:3000/#/others/info",
        "cancel_url": "http://localhost:3000/#/others/payment"
    }
    }
    
    print(token['access_token'])
    
    #change invoice number
    global invoice
    invoice = invoice+1
    
    #request for payment
    payment_link = requests.post(url=payment_url , headers=payment_header , json=payment_data)
    
    execute_url = payment_link.json()['links'][2]['href']
    return payment_link.json()['links']

#service to get payment link
@root.post('/getToken')
def generateToken(data:dict):
    global info
    info = data
    
    data['invoice'] = invoice
    print(data) 
       
    token_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    payload = {"grant_type":"client_credentials"}
    
    token = requests.post(url=token_url , auth=(secret.client_id,secret.secret_key),data=payload)
    return getLink(data,token.json())

#service to execute payment
@root.post('/execute')
def execute(data:dict , db:Session=Depends(get_db)):
    result = requests.post(url=execute_url , headers=payment_header , json=data)
    if(result.json().get('state')):
        information = {"firstname":result.json()['payer']['payer_info']['first_name'],"lastname":result.json()['payer']['payer_info']['last_name'],"email":result.json()['payer']['payer_info']['email'],"payment_method":result.json()['payer']['payment_method'],"paid_to":result.json()['transactions'][0]['payee']['email'],"paypal_id":result.json()['transactions'][0]['related_resources'][0]['sale']['id'],"amount":result.json()['transactions'][0]['amount']['total'],"mobile":info['mobileNumber'],"refund_link":result.json()['transactions'][0]['related_resources'][0]['sale']['links'][1]['href']}
        
        #to store db table
        payment_details:Transaction_info = information
        payment_info = PaymentData(**payment_details.dict())
        db.add(payment_info)
        db.commit()
        db.refresh(payment_info)
                
    else:
        info['message'] = result.json()['message'] 
        information = info  
            
    return information