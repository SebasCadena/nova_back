from pydantic import BaseModel, field_validator

class Create_User(BaseModel):
    """Schema para crear un nuevo usuario (sin ID)"""
    name: str
    email: str
    password: str
    role_id: int

    @field_validator('password')
    @classmethod
    def contrasena_max_length(cls, v):
        """Validar que la contraseña no exceda 72 bytes (límite de bcrypt)"""
        if len(v.encode('utf-8')) > 72:
            raise ValueError('La contraseña no puede exceder 72 caracteres')
        if len(v) < 4:
            raise ValueError('La contraseña debe tener al menos 4 caracteres')
        return v

class User(BaseModel):
    """Schema para usuario existente (con ID)"""
    id: int
    name: str
    email: str
    password: str
    role_id: int