# Bitácora de migración: PostgreSQL local -> Neon + ORM (SQLAlchemy) + FastAPI

> Proyecto: `nova_back`
> 
> Objetivo: migrar de SQLAlchemy Core (`Table`, `conn.execute`) a SQLAlchemy ORM (`Session`, modelos), dejando una base mantenible para Alembic y despliegue en Render.

---

## 1) Decisiones clave que tomamos

- Migración **completa a ORM** (sin capa de compatibilidad `.__table__`).
- Mantener **un único `Base`** para todos los modelos.
- Usar `Session` por request con `Depends(get_db)`.
- Dejar `DATABASE_URL` en `.env` apuntando a Neon con SSL.
- Forzar errores tempranos: si algo sigue en patrón viejo, que falle para corregirlo.

---

## 2) Conceptos importantes

### ¿Qué es `Base`?

- Es la clase padre de todos los modelos ORM (`User`, `Product`, etc.).
- De ahí sale `Base.metadata`, que contiene la definición de tablas/columnas/constraints del código.
- Alembic usa ese metadata para comparar modelos vs BD.

**No es** historial de cambios.
El historial lo lleva Alembic (`alembic/versions` + tabla `alembic_version`).

### ¿Dónde debe vivir `Base`?

- Recomendado: archivo dedicado en modelos, por ejemplo `models/base_model.py`.
- Regla de oro: **solo un `Base` en todo el proyecto**.

### ¿Qué es `Session`?

- Unidad de trabajo contra la BD en una request.
- Con `Session` haces `add`, `query/select`, `commit`, `rollback`, `refresh`.
- Se crea por request y se cierra al final.

---

## 3) Estructura recomendada

## `models/base_model.py`

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

## `config/config.py`

- Carga `.env`
- Crea `engine`
- Crea `SessionLocal`
- Expone `get_db`

Patrón:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

---

## 4) Patrón CRUD ORM en FastAPI

### GET (lista)

```python
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### GET by id

- Buscar por ID
- Si no existe: `404`

### POST (crear)

- `db.add(obj)`
- `db.commit()`
- `db.refresh(obj)`
- Devolver objeto serializado

### PUT/PATCH (actualizar)

- Buscar registro
- Mutar campos
- `db.commit()` + `db.refresh()`

### DELETE

- Buscar registro
- `db.delete(obj)`
- `db.commit()`

---

## 5) Reglas de transacciones (muy importantes)

- `commit` solo en escrituras (`POST/PUT/PATCH/DELETE`).
- Nunca hacer `commit` en lecturas (`GET`).
- Manejar `IntegrityError` en escrituras:
  - `rollback`
  - Responder `409` (duplicados) o `400` según caso.

---

## 6) Seguridad y serialización

- No devolver `password` en respuestas.
- Usar serializer/helper o schema de salida (`UserOut`).
- En login:
  - buscar usuario por email
  - verificar hash
  - emitir JWT

---

## 7) Neon + `.env`

Formato recomendado:

```dotenv
DATABASE_URL="postgresql://USER:PASSWORD@HOST/DB?sslmode=require"
```

En este proyecto también se está usando `channel_binding=require`, lo cual es válido si tu cliente/controlador lo soporta.

Buenas prácticas:

- No hardcodear credenciales en código.
- Rotar credenciales si se exponen por accidente.
- En Render, definir `DATABASE_URL` como variable de entorno.

---

## 8) Errores comunes que detectamos

- Tener dos `Base` distintos (rompe autogenerate/metadata).
- Mezclar `conn.execute(...)` (Core) con `Session` (ORM) en la misma capa.
- Mantener alias temporales como `Model.__table__` durante demasiado tiempo.
- Importar dependencias viejas como `get_connection` después de pasar a `get_db`.

---

## 9) Estado actual de migración (resumen)

- Modelos migrados a ORM.
- Alias de compatibilidad `.__table__` eliminados para forzar ORM puro.
- `users_router` migrado a `Session` + ORM.
- Siguiente paso: migrar routers restantes con el mismo patrón.

---

## 10) Checklist para cada router que migres

- [ ] Cambiar `Depends(get_connection)` por `Depends(get_db)`
- [ ] Cambiar import de `*_model` por clase ORM (`User`, `Category`, etc.)
- [ ] Reemplazar `conn.execute(...)` por operaciones `Session`
- [ ] Añadir manejo de `404` cuando no exista registro
- [ ] Añadir `IntegrityError` + `rollback` en escrituras
- [ ] Evitar devolver campos sensibles
- [ ] Verificar que no hay `commit` en GET

---

## 11) Tips prácticos para ir más rápido

- Migra 1 router completo y úsalo como plantilla para los demás.
- Mantén nombres consistentes: `Session db`, `get_db`, `Model` singular.
- Haz cambios pequeños y verificables por módulo (`users`, luego `categories`, etc.).
- Cuando termines un router, valida imports y errores antes de seguir.

---

## 12) Siguiente etapa sugerida

1. Migrar `categories_router` a ORM.
2. Migrar `products_router` y `services_router`.
3. Migrar flujo transaccional (`cart`, `orders`, `payments`).
4. Configurar Alembic con `Base.metadata` único y generar primera migración de control.

---

Si mantienes estas reglas, tendrás una base sólida para Neon + Render + Alembic sin deuda técnica de transición.
