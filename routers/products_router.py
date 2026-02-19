from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.products_model import product_model

product_router = APIRouter()

@product_router.get("/products")
def getProducts(conn: Connection = Depends(get_connection)):
    """Obtener todos los productos"""
    result = conn.execute(product_model.select()).fetchall()
    return [dict(row._mapping) for row in result]