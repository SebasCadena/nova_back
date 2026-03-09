from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.payments_model import Payment
from schemas.payments_schema import payment_schema

payment_router = APIRouter()

def _serialize_payment(payment: Payment) -> dict:
    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "provider": payment.provider,
        "status": payment.status,
        "amount": payment.amount,
        "created_at": payment.created_at,
    }

@payment_router.get("/payments")
def getPayments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return [_serialize_payment(payment) for payment in payments]


@payment_router.get("/payments/{idPayment}")
def getPaymentById(idPayment: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == idPayment).first()
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return _serialize_payment(payment)


@payment_router.post("/payments", status_code=status.HTTP_201_CREATED)
def createPayment(payment_data: payment_schema, db: Session = Depends(get_db)):
    new_payment = Payment(
        order_id=payment_data.order_id,
        provider=payment_data.provider,
        status=payment_data.status,
        amount=payment_data.amount,
    )
    db.add(new_payment)

    try:
        db.commit()
        db.refresh(new_payment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )

    return {"message": "Pago creado exitosamente", "idPayment": new_payment.id}


@payment_router.put("/payments/{idPayment}")
def updatePayment(idPayment: int, payment_data: payment_schema, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == idPayment).first()
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

    payment.order_id = payment_data.order_id
    payment.provider = payment_data.provider
    payment.status = payment_data.status
    payment.amount = payment_data.amount

    try:
        db.commit()
        db.refresh(payment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en los datos")

    return {"message": "Pago actualizado exitosamente", "payment": _serialize_payment(payment)}


@payment_router.delete("/payments/{idPayment}")
def deletePayment(idPayment: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == idPayment).first()
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

    db.delete(payment)
    db.commit()

    return {"message": "Pago eliminado exitosamente"}
