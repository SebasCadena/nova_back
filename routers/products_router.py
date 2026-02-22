from fastapi import APIRouter, Depends, HTTPException, status
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
    
    
# ----------------------------------------------------------------------------

@product_router.put("/products/{idProducto}")
def updateProduct(idProducto: int, product: product_schema, conn: Connection = Depends(get_connection)):
    """Actualizar un producto existente"""
    # Verificar que el producto existe
    existing = conn.execute(
        product_model.select().where(product_model.c.id == idProducto)
    ).first()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    updated_product = {
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price": product.price,
        "image_url": product.image_url,
        "category_id": product.category_id,
        "is_active": product.is_active
    }
    
    result = conn.execute(
        product_model.update().where(product_model.c.id == idProducto).values(updated_product)
    )
    conn.commit()
    
    return {"message": "Producto actualizado exitosamente"}