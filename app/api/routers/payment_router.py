from fastapi import APIRouter, HTTPException

from app.services.payment_service import(
    create_payment_order,
    # verify_payment
)

router = APIRouter(prefix="/api/payments",
                   tags=["Payments"]
                   )

@router.post("/create-order")
def create_order(amount:int):
    order = create_payment_order(amount)

    return{
        "order_id" : order["id"],
        "amount" : order["amount"],
        "currency" : order["currency"]
    }
