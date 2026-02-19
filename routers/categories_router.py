from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.categories_model import category_model

category_router = APIRouter()

@category_router.get("/categories")
def getCategories(conn: Connection = Depends(get_connection)):
    """Obtener todas las categorías"""
    result = conn.execute(category_model.select()).fetchall()
    return [dict(row._mapping) for row in result]