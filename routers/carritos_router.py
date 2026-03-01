from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.carritos_model import carrito_model
from schemas.carritos_schemas import carrito_schema

carrito_router = APIRouter()

@carrito_router.get("/carritos")
def getCarritos(conn: Connection = Depends(get_connection)):
    """Obtener todos los carritos"""
    result = conn.execute(carrito_model.select()).fetchall()
    return [dict(row._mapping) for row in result]


@carrito_router.post("/carritos", status_code=status.HTTP_201_CREATED)
def createCarrito(carrito_data: carrito_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo carrito"""
    new_carrito = {
        "user_id": carrito_data.user_id,
    }

    try:
        result = conn.execute(
            carrito_model.insert().values(new_carrito).returning(carrito_model.c.id)
        )
        new_id = result.fetchone()[0]

        return {
            "message": "Carrito creado exitosamente",
            "idCarrito": new_id
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
