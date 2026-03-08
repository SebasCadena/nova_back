from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.order_items_model import OrderItem
from schemas.order_items_schema import order_item_schema

order_items_router = APIRouter()

def _serialize_order_item(order_item: OrderItem) -> dict:
    return {
        "id": order_item.id,
        "order_id": order_item.order_id,
        "product_id": order_item.product_id,
        "quantity": order_item.quantity,
        "price": order_item.price,
    }

@order_items_router.get("/order-items")
def getOrderItems(db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).all()
    return [_serialize_order_item(order_item) for order_item in order_items]


@order_items_router.get("/order-items/{idOrderItem}")
def getOrderItemById(idOrderItem: int, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == idOrderItem).first()
    if order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de orden no encontrado")
    return _serialize_order_item(order_item)


@order_items_router.post("/order-items", status_code=status.HTTP_201_CREATED)
def createOrderItem(order_item_data: order_item_schema, db: Session = Depends(get_db)):
    new_order_item = OrderItem(
        order_id=order_item_data.order_id,
        product_id=order_item_data.product_id,
        quantity=order_item_data.quantity,
        price=order_item_data.price,
    )
    db.add(new_order_item)

    try:
        db.commit()
        db.refresh(new_order_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )

    return {"message": "Item de orden creado exitosamente", "idOrderItem": new_order_item.id}


@order_items_router.put("/order-items/{idOrderItem}")
def updateOrderItem(idOrderItem: int, order_item_data: order_item_schema, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == idOrderItem).first()
    if order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de orden no encontrado")

    order_item.order_id = order_item_data.order_id
    order_item.product_id = order_item_data.product_id
    order_item.quantity = order_item_data.quantity
    order_item.price = order_item_data.price

    try:
        db.commit()
        db.refresh(order_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en los datos")

    return {"message": "Item de orden actualizado exitosamente", "orderItem": _serialize_order_item(order_item)}


@order_items_router.delete("/order-items/{idOrderItem}")
def deleteOrderItem(idOrderItem: int, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == idOrderItem).first()
    if order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de orden no encontrado")

    db.delete(order_item)
    db.commit()

    return {"message": "Item de orden eliminado exitosamente"}
