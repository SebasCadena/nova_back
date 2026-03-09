from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.roles import require_admin
from config.config import get_db
from models.categories_model import Category
from schemas.categories_schemas import category_schema

category_router = APIRouter()

def _serialize_category(category: Category) -> dict:
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }

@category_router.get("/categories")
def getCategories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [_serialize_category(category) for category in categories]


@category_router.get("/categories/{idCategoria}")
def getCategoryById(idCategoria: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == idCategoria).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return _serialize_category(category)

# ------------------------------------------------------------------

@category_router.post("/categories", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def createCategory(category_data: category_schema, db: Session = Depends(get_db)):
    new_category = Category(name=category_data.name, slug=category_data.slug)
    db.add(new_category)
    try:
        db.commit()
        db.refresh(new_category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nombre o slug ya existen")

    return {"message": "Categoría creada exitosamente", "idCategoria": new_category.id}


# -------------------------------------------------------------------------

@category_router.put("/categories/{idCategoria}", dependencies=[Depends(require_admin)])
def updateCategory(idCategoria: int, category_data: category_schema, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == idCategoria).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    category.name = category_data.name
    category.slug = category_data.slug
    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nombre o slug ya existen")

    return {"message": "Categoría actualizada exitosamente", "category": _serialize_category(category)}

# ---------------------------------------------------------------------------

@category_router.delete("/categories/{idCategoria}", dependencies=[Depends(require_admin)])
def deleteCategory(idCategoria: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == idCategoria).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")

    db.delete(category)
    db.commit()

    return {"message": "Categoría eliminada exitosamente"}