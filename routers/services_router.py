from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from config.config import get_connection
from models.services_model import service as service_table
from schemas.services_schema import service

service_router = APIRouter()

@service_router.get("/services")
def getServices(conn: Connection = Depends(get_connection)):
    """Obtener todos los servicios"""
    result = conn.execute(service_table.select()).fetchall()
    return [dict(row._mapping) for row in result]

# -----------------------------------------------------------------------

@service_router.post("/services", status_code=status.HTTP_201_CREATED)
def createService(service_data: service, conn: Connection = Depends(get_connection)):
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
            service_table.insert().values(new_service).returning(service_table.c.id)
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