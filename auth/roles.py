from enum import IntEnum

from fastapi import Depends, HTTPException, status

from auth.bearer import get_current_user


class Role(IntEnum):
    CUSTOMER = 0
    ADMIN = 1
    
    
def require_admin(current_user: dict = Depends(get_current_user)):
    role_id = int(current_user.get("role_id", -1))
    if role_id != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para administradores",
        )
    return current_user