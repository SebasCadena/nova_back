from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.config import get_db
from models.services_model import Service
from schemas.services_schema import service_schema

service_router = APIRouter()

def _serialize_service(service: Service) -> dict:
    return {
        "id": service.id,
        "title": service.title,
        "slug": service.slug,
        "description": service.description,
        "icon": service.icon,
        "is_active": service.is_active,
        "short_description": service.short_description,
        "price": service.price,
        "features": service.features,
        "created_at": service.created_at,
        "updated_at": service.updated_at,
    }

@service_router.get("/services")
def getServices(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return [_serialize_service(service) for service in services]


@service_router.get("/services/{idServicio}")
def getServiceById(idServicio: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == idServicio).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")
    return _serialize_service(service)

# -----------------------------------------------------------------------

@service_router.post("/services", status_code=status.HTTP_201_CREATED)
def createService(service_data: service_schema, db: Session = Depends(get_db)):
    new_service = Service(
        title=service_data.title,
        slug=service_data.slug,
        description=service_data.description,
        icon=service_data.icon,
        is_active=service_data.is_active,
        short_description=service_data.short_description,
        price=service_data.price,
        features=service_data.features,
    )
    db.add(new_service)

    try:
        db.commit()
        db.refresh(new_service)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un servicio con ese título o slug")

    return {"message": "Servicio creado exitosamente", "idServicio": new_service.id}
        
        
# ----------------------------------------------------------------------------

@service_router.put("/services/{idServicio}")
def updateService(idServicio: int, service_data: service_schema, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == idServicio).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")

    service.title = service_data.title
    service.slug = service_data.slug
    service.description = service_data.description
    service.icon = service_data.icon
    service.is_active = service_data.is_active
    service.short_description = service_data.short_description
    service.price = service_data.price
    service.features = service_data.features

    try:
        db.commit()
        db.refresh(service)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un servicio con ese título o slug")

    return {"message": "Servicio actualizado exitosamente", "service": _serialize_service(service)}

# --------------------------------------------------------------------------------

@service_router.delete("/services/{idServicio}")
def deleteService(idServicio: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == idServicio).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")

    db.delete(service)
    db.commit()

    return {"message": "Servicio eliminado exitosamente"}