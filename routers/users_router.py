from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from config.config import get_connection
from models.users_model import user
from schemas.users_schema import User, Create_User

from sqlalchemy.engine import Connection

from datetime import timedelta
from auth.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from auth.bearer import get_current_user

user_router = APIRouter()

# 🔓 RUTAS PÚBLICAS (sin protección)

class LoginRequest(BaseModel):
    email: str
    password: str

@user_router.post("/login")
def login(login_data: LoginRequest, conn: Connection = Depends(get_connection)):
    """Login que devuelve un token JWT"""
    result = conn.execute(
        user.select().where(user.c.email == login_data.email)
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    user_data = dict(result._mapping)
    
    # Verificar contrasena (asume que están hasheadas en BD)
    if not verify_password(login_data.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["email"], "id": user_data["id"], "role_id": user_data["role_id"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_data["id"],
            "name": user_data["name"],
            "email": user_data["email"],
            "role_id": user_data["role_id"]
        }
    }

@user_router.post("/users")
def createUser(user_data: Create_User, conn: Connection = Depends(get_connection)):
    """Crear usuario con contrasena hasheada"""
    new_user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": get_password_hash(user_data.password),  # 🔒 Hashear contrasena
        "role_id": user_data.role_id
    }
    result = conn.execute(user.insert().values(new_user))
    conn.commit()
    return {"message": "Usuario creado exitosamente"}



@user_router.get("/users")
def getUsers(current_user: dict = Depends(get_current_user), conn: Connection = Depends(get_connection)):
    """Solo usuarios autenticados pueden ver la lista"""
    result = conn.execute(user.select()).fetchall()
    return [dict(row._mapping) for row in result]
