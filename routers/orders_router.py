from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.orders_model import Order
from schemas.orders_schema import order_schema

order_router = APIRouter()

def _serialize_order(order: Order) -> dict:
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "total": order.total,
        "created_at": order.created_at,
    }

@order_router.get("/orders")
def getOrders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [_serialize_order(order) for order in orders]


@order_router.get("/orders/{idOrder}")
def getOrderById(idOrder: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == idOrder).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return _serialize_order(order)


@order_router.post("/orders", status_code=status.HTTP_201_CREATED)
def createOrder(order_data: order_schema, db: Session = Depends(get_db)):
    new_order = Order(
        user_id=order_data.user_id,
        status=order_data.status,
        total=order_data.total,
        created_at=order_data.created_at,
    )
    db.add(new_order)

    try:
        db.commit()
        db.refresh(new_order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )

    return {"message": "Orden creada exitosamente", "idOrder": new_order.id}


@order_router.put("/orders/{idOrder}")
def updateOrder(idOrder: int, order_data: order_schema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == idOrder).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

    order.user_id = order_data.user_id
    order.status = order_data.status
    order.total = order_data.total

    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en los datos")

    return {"message": "Orden actualizada exitosamente", "order": _serialize_order(order)}


@order_router.delete("/orders/{idOrder}")
def deleteOrder(idOrder: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == idOrder).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

    db.delete(order)
    db.commit()

    return {"message": "Orden eliminada exitosamente"}
