from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.categories_model import category_model
from schemas.categories_schemas import category_schema

category_router = APIRouter()

@category_router.get("/categories")
def getCategories(conn: Connection = Depends(get_connection)):
    """Obtener todas las categorías"""
    result = conn.execute(category_model.select()).fetchall()
    return [dict(row._mapping) for row in result]

# ------------------------------------------------------------------

@category_router.post("/categories", status_code=status.HTTP_201_CREATED)
def createCategory(category_data: category_schema, conn: Connection = Depends(get_connection)):
    """Crear una nueva categoría"""
    
    
    new_category = {
        "name": category_data.name,
        "slug": category_data.slug,
    }
    
    
    # En PostgreSQL usamos RETURNING para obtener el ID generado
    result = conn.execute(
        category_model.insert().values(new_category).returning(category_model.c.id)
    )
        
        # Obtener el ID de la categoría recién creada
    new_id = result.fetchone()[0]
        
    return {
        "message": "Categoría creada exitosamente",
        "idCategoria": new_id
    }
    