from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.cart_items_model import CartItem
from schemas.cart_items_schema import cart_item_schema

cart_items_router = APIRouter()

def _serialize_cart_item(cart_item: CartItem) -> dict:
    return {
        "id": cart_item.id,
        "cart_id": cart_item.cart_id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
    }

@cart_items_router.get("/cart-items")
def getCartItems(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    return [_serialize_cart_item(cart_item) for cart_item in cart_items]


@cart_items_router.get("/cart-items/{idCartItem}")
def getCartItemById(idCartItem: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == idCartItem).first()
    if cart_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de carrito no encontrado")
    return _serialize_cart_item(cart_item)


@cart_items_router.post("/cart-items", status_code=status.HTTP_201_CREATED)
def createCartItem(cart_item_data: cart_item_schema, db: Session = Depends(get_db)):
    new_cart_item = CartItem(
        cart_id=cart_item_data.cart_id,
        product_id=cart_item_data.product_id,
        quantity=cart_item_data.quantity,
    )
    db.add(new_cart_item)

    try:
        db.commit()
        db.refresh(new_cart_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )

    return {"message": "Item de carrito creado exitosamente", "idCartItem": new_cart_item.id}


@cart_items_router.put("/cart-items/{idCartItem}")
def updateCartItem(idCartItem: int, cart_item_data: cart_item_schema, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == idCartItem).first()
    if cart_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de carrito no encontrado")

    cart_item.cart_id = cart_item_data.cart_id
    cart_item.product_id = cart_item_data.product_id
    cart_item.quantity = cart_item_data.quantity

    try:
        db.commit()
        db.refresh(cart_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en los datos")

    return {"message": "Item de carrito actualizado exitosamente", "cartItem": _serialize_cart_item(cart_item)}


@cart_items_router.delete("/cart-items/{idCartItem}")
def deleteCartItem(idCartItem: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartItem).filter(CartItem.id == idCartItem).first()
    if cart_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item de carrito no encontrado")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item de carrito eliminado exitosamente"}
