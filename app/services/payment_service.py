import razorpay

from app.core.config import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
)

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET)
)

def create_payment_order(amount:int):
    data={
        "amount" : amount*100,
        "currency": "INR",
        "receipt": "transport_receipt"
    }
    order = client.order.create(data=data)
    return order
