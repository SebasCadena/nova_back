from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.order_items_model import order_items_model
from schemas.order_items_schema import order_item_schema

order_items_router = APIRouter()

@order_items_router.get("/order-items")
def getOrderItems(conn: Connection = Depends(get_connection)):
    """Obtener todos los items de orden"""
    result = conn.execute(order_items_model.select()).fetchall()
    return [dict(row._mapping) for row in result]


@order_items_router.post("/order-items", status_code=status.HTTP_201_CREATED)
def createOrderItem(order_item_data: order_item_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo item de orden"""
    new_order_item = {
        "order_id": order_item_data.order_id,
        "product_id": order_item_data.product_id,
        "quantity": order_item_data.quantity,
        "price": order_item_data.price,
    }

    try:
        result = conn.execute(
            order_items_model.insert().values(new_order_item).returning(order_items_model.c.id)
        )
        new_id = result.fetchone()[0]

        return {
            "message": "Item de orden creado exitosamente",
            "idOrderItem": new_id
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
