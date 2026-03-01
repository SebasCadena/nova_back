from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.payments_model import payment_model
from schemas.payments_schema import payment_schema

payment_router = APIRouter()

@payment_router.get("/payments")
def getPayments(conn: Connection = Depends(get_connection)):
    """Obtener todos los pagos"""
    result = conn.execute(payment_model.select()).fetchall()
    return [dict(row._mapping) for row in result]


@payment_router.post("/payments", status_code=status.HTTP_201_CREATED)
def createPayment(payment_data: payment_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo pago"""
    new_payment = {
        "order_id": payment_data.order_id,
    }

    if payment_data.provider is not None:
        new_payment["provider"] = payment_data.provider
    if payment_data.status is not None:
        new_payment["status"] = payment_data.status
    if payment_data.amount is not None:
        new_payment["amount"] = payment_data.amount
    if payment_data.created_at is not None:
        new_payment["created_at"] = payment_data.created_at

    try:
        result = conn.execute(
            payment_model.insert().values(new_payment).returning(payment_model.c.id)
        )
        new_id = result.fetchone()[0]

        return {
            "message": "Pago creado exitosamente",
            "idPayment": new_id
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
