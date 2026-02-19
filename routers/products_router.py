from fastapi import APIRouter, Depends, status
from sqlalchemy.engine import Connection
from config.config import get_connection
from models.products_model import product_model
from schemas.products_schema import product_schema

product_router = APIRouter()

@product_router.get("/products")
def getProducts(conn: Connection = Depends(get_connection)):
    """Obtener todos los productos"""
    result = conn.execute(product_model.select()).fetchall()
    return [dict(row._mapping) for row in result]

# ------------------------------------------------------------------

@product_router.post("/products", status_code=status.HTTP_201_CREATED)
def createProduct(product_data: product_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo producto"""
    
    
    new_product = {
        "name": product_data.name,
        "slug": product_data.slug,
        "description": product_data.description,
        "price": product_data.price,
        "image_url": product_data.image_url,
        "category_id": product_data.category_id,
        "is_active": product_data.is_active
    }
    
    
    # En PostgreSQL usamos RETURNING para obtener el ID generado
    result = conn.execute(
        product_model.insert().values(new_product).returning(product_model.c.id)
    )
        
        # Obtener el ID del producto recién creado
    new_id = result.fetchone()[0]
        
    return {
        "message": "Producto creado exitosamente",
        "idProducto": new_id
    }