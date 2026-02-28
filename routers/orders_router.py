from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.orders_model import order_model
from schemas.orders_schema import order_schema

order_router = APIRouter()

@order_router.get("/orders")
def getOrders(conn: Connection = Depends(get_connection)):
    """Obtener todas las ordenes"""
    result = conn.execute(order_model.select()).fetchall()
    return [dict(row._mapping) for row in result]


@order_router.post("/orders", status_code=status.HTTP_201_CREATED)
def createOrder(order_data: order_schema, conn: Connection = Depends(get_connection)):
    """Crear una nueva orden"""
    new_order = {
        "user_id": order_data.user_id,
        "status": order_data.status,
        "total": order_data.total,
    }

    if order_data.created_at is not None:
        new_order["created_at"] = order_data.created_at

    try:
        result = conn.execute(
            order_model.insert().values(new_order).returning(order_model.c.id)
        )
        new_id = result.fetchone()[0]

        return {
            "message": "Orden creada exitosamente",
            "idOrder": new_id
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
