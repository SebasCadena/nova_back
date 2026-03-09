from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.roles import require_admin
from config.config import get_db
from models.products_model import Product
from schemas.products_schema import product_schema

product_router = APIRouter()

def _serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price": product.price,
        "image_url": product.image_url,
        "category_id": product.category_id,
        "is_active": product.is_active,
        "stok": product.stok,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }

@product_router.get("/products")
def getProducts(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [_serialize_product(product) for product in products]


@product_router.get("/products/{idProducto}")
def getProductById(idProducto: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == idProducto).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return _serialize_product(product)

# ------------------------------------------------------------------

@product_router.post("/products", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def createProduct(product_data: product_schema, db: Session = Depends(get_db)):
    new_product = Product(
        name=product_data.name,
        slug=product_data.slug,
        description=product_data.description,
        price=float(product_data.price),
        image_url=product_data.image_url,
        category_id=product_data.category_id,
        is_active=product_data.is_active,
        stok=product_data.stok,
    )
    db.add(new_product)

    try:
        db.commit()
        db.refresh(new_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nombre o slug ya existen")

    return {"message": "Producto creado exitosamente", "idProducto": new_product.id}
    
    
# ----------------------------------------------------------------------------

@product_router.put("/products/{idProducto}", dependencies=[Depends(require_admin)])
def updateProduct(idProducto: int, product_data: product_schema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == idProducto).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    product.name = product_data.name
    product.slug = product_data.slug
    product.description = product_data.description
    product.price = float(product_data.price)
    product.image_url = product_data.image_url
    product.category_id = product_data.category_id
    product.is_active = product_data.is_active
    product.stok = product_data.stok

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nombre o slug ya existen")

    return {"message": "Producto actualizado exitosamente", "product": _serialize_product(product)}

# -------------------------------------------------------------------------

@product_router.delete("/products/{idProducto}", dependencies=[Depends(require_admin)])
def deleteProduct(idProducto: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == idProducto).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    db.delete(product)
    db.commit()

    return {"message": "Producto eliminado exitosamente"}