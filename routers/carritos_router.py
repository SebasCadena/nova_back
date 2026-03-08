from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.carritos_model import Cart
from schemas.carritos_schemas import carrito_schema

carrito_router = APIRouter()

def _serialize_cart(cart: Cart) -> dict:
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "created_at": cart.created_at,
        "updated_at": cart.updated_at,
    }

@carrito_router.get("/carritos")
def getCarritos(db: Session = Depends(get_db)):
    carts = db.query(Cart).all()
    return [_serialize_cart(cart) for cart in carts]


@carrito_router.get("/carritos/{idCarrito}")
def getCarritoById(idCarrito: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == idCarrito).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    return _serialize_cart(cart)


@carrito_router.post("/carritos", status_code=status.HTTP_201_CREATED)
def createCarrito(carrito_data: carrito_schema, db: Session = Depends(get_db)):
    new_carrito = Cart(user_id=carrito_data.user_id)
    db.add(new_carrito)

    try:
        db.commit()
        db.refresh(new_carrito)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de integridad en los datos"
        )

    return {"message": "Carrito creado exitosamente", "idCarrito": new_carrito.id}


@carrito_router.put("/carritos/{idCarrito}")
def updateCarrito(idCarrito: int, carrito_data: carrito_schema, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == idCarrito).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

    cart.user_id = carrito_data.user_id
    try:
        db.commit()
        db.refresh(cart)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error de integridad en los datos")

    return {"message": "Carrito actualizado exitosamente", "cart": _serialize_cart(cart)}


@carrito_router.delete("/carritos/{idCarrito}")
def deleteCarrito(idCarrito: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == idCarrito).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

    db.delete(cart)
    db.commit()

    return {"message": "Carrito eliminado exitosamente"}
