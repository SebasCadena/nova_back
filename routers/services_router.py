from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from config.config import get_connection
from models.services_model import service_model
from schemas.services_schema import service_schema

service_router = APIRouter()

@service_router.get("/services")
def getServices(conn: Connection = Depends(get_connection)):
    """Obtener todos los servicios"""
    result = conn.execute(service_model.select()).fetchall()
    return [dict(row._mapping) for row in result]

# -----------------------------------------------------------------------

@service_router.post("/services", status_code=status.HTTP_201_CREATED)
def createService(service_data: service_schema, conn: Connection = Depends(get_connection)):
    """Crear un nuevo servicio"""
    
    
    new_service = {
        "title": service_data.title,
        "slug": service_data.slug,
        "description": service_data.description,
        "icon": service_data.icon,
        "is_active": service_data.is_active,
        "short_description": service_data.short_description,
        "price": service_data.price,
        "features": service_data.features
    }
    
    try:
        # En PostgreSQL usamos RETURNING para obtener el ID generado
        result = conn.execute(
            service_model.insert().values(new_service).returning(service_model.c.id)
        )
        
        # Obtener el ID del servicio recién creado
        new_id = result.fetchone()[0]
        
        return {
            "message": "Servicio creado exitosamente",
            "idServicio": new_id
        }
    except IntegrityError as e:
        # Manejar errores de duplicados u otras violaciones de integridad
        if "duplicate key" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un servicio con ese título o slug"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos"
        )
        
        
# ----------------------------------------------------------------------------

@service_router.put("/services/{idServicio}")
def updateService(idServicio: int, service: service_schema, conn: Connection = Depends(get_connection)):
    """Actualizar un servicio existente"""
    # Verificar que el servicio existe
    existing = conn.execute(
        service_model.select().where(service_model.c.id == idServicio)
    ).first()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado"
        )
    
    updated_service = {
        "title": service.title,
        "slug": service.slug,
        "description": service.description,
        "icon": service.icon,
        "is_active": service.is_active,
        "short_description": service.short_description,
        "price": service.price,
        "features": service.features
    }
    
    result = conn.execute(
        service_model.update().where(service_model.c.id == idServicio).values(updated_service)
    )
    conn.commit()
    
    return {"message": "Servicio actualizado exitosamente"}

# --------------------------------------------------------------------------------

@service_router.delete("/services/{idServicio}")
def deleteService(idServicio: int, conn: Connection = Depends(get_connection)):
    """Eliminar un servicio"""
    result = conn.execute(
        service_model.delete().where(service_model.c.id == idServicio)
    )
    conn.commit()
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado"
        )
    
    return {"message": "Servicio eliminado exitosamente"}