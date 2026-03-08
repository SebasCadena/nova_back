# Auditoria de Seguridad y Produccion - NOVA Backend

Fecha: 2026-03-08  
Proyecto: `nova_back` (FastAPI + SQLAlchemy + Postgres)

## Resumen Ejecutivo

Estado recomendado para salida a produccion: `NO-GO` (aun no listo para trafico real de clientes).

La base del proyecto esta bien encaminada (CRUDs, JWT, migraciones), pero faltan controles clave de seguridad y operacion. Este documento esta pensado para que lo uses como guia de aprendizaje y ejecucion.

---

## Hallazgos Criticos (bloquean salida)

## 1) Secreto JWT hardcodeado
- Evidencia: `auth/auth.py` (`SECRET_KEY = "CLAVESECRETA"`)
- Riesgo: si el codigo se filtra, cualquiera podria firmar tokens validos.
- Solucion:
1. Mover `SECRET_KEY` a variable de entorno.
2. Fallar al iniciar si no existe la variable.
3. Rotar la clave actual antes de pasar a produccion.

Ejemplo de enfoque:
```python
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no configurada")
```

## 2) CORS abierto a todo
- Evidencia: `app.py` (`allow_origins=["*"]`, metodos y headers abiertos)
- Riesgo: cualquier origen puede intentar consumir tu API desde navegador.
- Solucion:
1. Definir lista explicita de dominios frontend permitidos.
2. Usar variables de entorno por ambiente (`dev`, `staging`, `prod`).
3. No dejar `*` en produccion.

## 3) Endpoints sensibles sin autenticacion
- Evidencia: routers de `orders`, `payments`, `products`, `services`, `carritos`, `cart_items`, `order_items` no usan `Depends(get_current_user)` en sus endpoints.
- Riesgo: cualquier persona puede leer, crear, modificar o borrar datos.
- Solucion:
1. Proteger endpoints con `Depends(get_current_user)`.
2. Separar rutas publicas (ej: catalogo) de rutas privadas.
3. Aplicar principio de minimo privilegio por endpoint.

## 4) Escalada de privilegios en registro de usuario
- Evidencia: `POST /users` recibe `role_id` del cliente.
- Riesgo: un usuario podria registrarse como admin si envia `role_id` alto.
- Solucion:
1. Quitar `role_id` del schema de registro publico.
2. Asignar `role_id` por backend (por defecto: cliente).
3. Crear endpoint admin separado para cambiar roles.

---

## Hallazgos Altos

## 5) Hay autenticacion, pero no autorizacion fina
- Evidencia: en `users_router.py` se valida token, pero no se valida propiedad del recurso ni rol para acciones criticas.
- Riesgo: usuario autenticado puede acceder/modificar datos que no le pertenecen.
- Solucion:
1. Agregar helpers de autorizacion (`require_admin`, `require_owner_or_admin`).
2. Validar ownership en carritos, ordenes, pagos.
3. Evitar que usuarios normales consulten listas globales completas.

## 6) Campos de auditoria controlados por el cliente
- Evidencia: en ordenes/pagos se acepta y asigna `created_at` desde request.
- Riesgo: un cliente puede falsear tiempos de negocio/auditoria.
- Solucion:
1. Eliminar `created_at` de schemas de entrada.
2. Dejar que DB asigne `CURRENT_TIMESTAMP`.
3. No permitir update manual de campos de auditoria.

## 7) Inconsistencia de tipos monetarios
- Evidencia:
1. `products.price` usa `Float`.
2. `services.price` usa `str`.
3. `orders.total` y `payments.amount` usan `Numeric(10,2)`.
- Riesgo: errores de redondeo, datos inconsistentes, bugs de facturacion.
- Solucion:
1. Estandarizar dinero en DB como `Numeric(10,2)`.
2. En Pydantic usar `Decimal`.
3. Normalizar conversiones en routers.

## 8) Politica de password debil
- Evidencia: minimo de 4 caracteres en `schemas/users_schema.py`.
- Riesgo: contrasenas facilmente rompibles.
- Solucion:
1. Exigir minimo 10-12 caracteres.
2. Pedir complejidad basica (mayuscula, minuscula, numero, simbolo) o passphrases fuertes.
3. Bloqueo temporal o rate limiting tras intentos fallidos de login.

## 9) Dependencias JWT potencialmente conflictivas
- Evidencia: `requirements.txt` incluye `jose==1.0.0` y `python-jose==3.5.0`.
- Riesgo: ambiguedad de importaciones y mantenimiento.
- Solucion:
1. Mantener solo `python-jose` si ese es el paquete usado.
2. Limpiar lock/dependencias y probar login/token.

---

## Hallazgos Medios (operacion y madurez)

## 10) Sin pruebas automatizadas
- Evidencia: no se detectaron `test*.py` ni pipeline CI.
- Riesgo: cambios rompen funcionalidad sin aviso.
- Solucion:
1. Crear tests base con `pytest` + `httpx` para login, permisos y CRUDs criticos.
2. Agregar workflow CI (lint + tests) en cada push/PR.

## 11) Sin endpoint de salud real
- Evidencia: solo existe `GET /`.
- Riesgo: no hay chequeo claro para orquestador/monitoring.
- Solucion:
1. Crear `/healthz` (app viva) y `/readyz` (DB disponible).
2. Usarlos en despliegue y monitoreo.

## 12) Logging y observabilidad basicos
- Evidencia: no se vio configuracion de logging de aplicacion.
- Riesgo: dificil investigar incidentes o errores en produccion.
- Solucion:
1. Configurar logs estructurados (JSON o formato consistente).
2. Registrar request-id, endpoint, status, latencia.
3. Evitar loggear datos sensibles (passwords, tokens completos).

## 13) Sin rate limiting ni proteccion anti abuso
- Evidencia: no se detecto limitador de solicitudes.
- Riesgo: abuso de login, scraping, consumo excesivo.
- Solucion:
1. Agregar rate limiting por IP/usuario, sobre todo en `/login`.
2. Definir limites distintos para lectura y escritura.

---

## Plan de Mejora Recomendado (en orden)

## Fase 1 (1-2 dias, impacto alto)
1. Mover secretos a `.env` y endurecer configuracion de arranque.
2. Cerrar CORS para dominios reales.
3. Proteger endpoints criticos con JWT.
4. Quitar `role_id` del registro publico.

## Fase 2 (3-5 dias)
1. Implementar autorizacion por rol y ownership.
2. Eliminar `created_at` de requests.
3. Unificar manejo de dinero con `Decimal/Numeric`.
4. Fortalecer reglas de password.

## Fase 3 (1 semana)
1. Agregar tests automatizados de seguridad y negocio.
2. Agregar `/healthz` y `/readyz`.
3. Configurar logging y alertas basicas.
4. Agregar rate limiting.

---

## Recomendaciones Generales (para aprender y mejorar rapido)

1. Prioriza seguridad por capas:
- Capa 1: autenticacion (quien eres).
- Capa 2: autorizacion (que puedes hacer).
- Capa 3: validacion (que datos permito).
- Capa 4: auditoria (que paso y cuando).

2. No confies en el frontend:
- Todo lo importante (roles, ownership, timestamps, montos finales) debe validarse en backend.

3. Trabaja con checklist de release:
- Secretos fuera del repo.
- CORS cerrado.
- Endpoints sensibles protegidos.
- Tests minimos corriendo.
- Migraciones aplicadas y verificadas.
- Health checks listos.

4. Define entornos claros:
- `dev`, `staging`, `prod` con variables y dominios distintos.

5. Construye por iteraciones pequenas:
- Cambios pequenos + test rapido + commit claro.

---

## Checklist de salida a produccion

- [ ] JWT secret desde entorno y rotado
- [ ] CORS restringido a dominios reales
- [ ] Endpoints sensibles protegidos con token
- [ ] Autorizacion por rol/ownership implementada
- [ ] Registro publico sin `role_id`
- [ ] `created_at` solo backend/DB
- [ ] Dinero en `Decimal/Numeric` de forma consistente
- [ ] Politica de password robusta
- [ ] Tests minimos automatizados
- [ ] Logging basico de requests/errores
- [ ] Health checks (`/healthz`, `/readyz`)
- [ ] Rate limiting en login y endpoints sensibles

---

## Nota final para tu contexto (estudiante)

Vas por buen camino. Llegar a este punto con backend funcional ya es un avance grande. En proyectos reales, el salto entre "funciona" y "listo para produccion" casi siempre esta en seguridad, observabilidad y calidad operativa, no solo en crear endpoints.

Si aplicas las Fases 1 y 2, tu API pasara de "demo funcional" a "base profesional solida".
