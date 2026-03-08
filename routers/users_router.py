from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from auth.bearer import get_current_user
from config.config import get_db
from models.users_model import User
from schemas.users_schema import Create_User

user_router = APIRouter()

# ------------------------
# DTOs de la ruta /login
# ------------------------

class LoginRequest(BaseModel):
    email: str
    password: str

def _serialize_user(user: User) -> dict:
    """Retorna una representación segura del usuario (sin password)."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role_id": user.role_id,
        "created_at": user.created_at,
    }

@user_router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica usuario y retorna token JWT."""
    user = db.query(User).filter(User.email == login_data.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "role_id": user.role_id},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": _serialize_user(user),
    }

@user_router.post("/users")
def createUser(user_data: Create_User, db: Session = Depends(get_db)):
    """Crea usuario con password hasheada (write -> commit)."""
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        role_id=user_data.role_id,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )

    return {
        "message": "Usuario creado exitosamente",
        "user": _serialize_user(new_user),
    }



@user_router.get("/users")
def getUsers(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lista usuarios (read-only -> sin commit)."""
    users = db.query(User).all()
    return [_serialize_user(user) for user in users]


@user_router.get("/users/{user_id}")
def getUserById(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obtiene un usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return _serialize_user(user)


@user_router.put("/users/{user_id}")
def updateUser(user_id: int, user_data: Create_User, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Actualiza usuario y hace commit de la transacción."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    user.name = user_data.name
    user.email = user_data.email
    user.password = get_password_hash(user_data.password)
    user.role_id = user_data.role_id

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )

    return {
        "message": "Usuario actualizado exitosamente",
        "user": _serialize_user(user),
    }


@user_router.delete("/users/{user_id}")
def deleteUser(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Elimina usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    db.delete(user)
    db.commit()

    return {"message": "Usuario eliminado exitosamente"}
