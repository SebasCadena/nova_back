from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.cart_items_model import cart_items_model
from schemas.cart_items_schema import cart_item_schema

cart_items_router = APIRouter()

@cart_items_router.get("/cart-items")
def getCartItems(conn: Connection = Depends(get_connection)):
    """Obtener todos los items de carrito"""
    result = conn.execute(cart_items_model.select()).fetchall()
    return [dict(row._mapping) for row in result]


@cart_items_router.post("/cart-items", status_code=status.HTTP_201_CREATED)
def createCartItem(cart_item_data: cart_item_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo item de carrito"""
    new_cart_item = {
        "cart_id": cart_item_data.cart_id,
        "product_id": cart_item_data.product_id,
        "quantity": cart_item_data.quantity,
    }

    try:
        result = conn.execute(
            cart_items_model.insert().values(new_cart_item).returning(cart_items_model.c.id)
        )
        new_id = result.fetchone()[0]

        return {
            "message": "Item de carrito creado exitosamente",
            "idCartItem": new_id
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
