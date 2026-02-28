# 🐳 Guía Completa: Dockerización del Backend NOVA

**Fecha:** 27 de febrero de 2026  
**Proyecto:** NOVA Backend  
**Base:** FastAPI + PostgreSQL  

---

## 📋 Tabla de Contenidos

1. [¿Por qué Docker?](#por-qué-docker)
2. [Requisitos previos](#requisitos-previos)
3. [Instalación de Docker](#instalación-de-docker)
4. [Archivos creados](#archivos-creados)
5. [Configuración explicada](#configuración-explicada)
6. [Cómo ejecutar](#cómo-ejecutar)
7. [Comandos útiles](#comandos-útiles)
8. [Troubleshooting](#troubleshooting)

---

## ¿Por qué Docker?

Docker es un contenedor que "empaqueta" tu aplicación completa con todas sus dependencias. Ventajas principales:

| Ventaja | Descripción |
|---------|-------------|
| **Reproducibilidad** | Tu app en desarrollo funciona exactamente igual en producción |
| **Fácil deployment** | De tu PC al servidor con el mismo comando |
| **Aislamiento** | Tu app no interfiere con otros servicios |
| **Escalabilidad** | Puedes levantar múltiples instancias fácilmente |
| **Versionado** | Exactamente qué imagen estás usando en producción |
| **Portabilidad** | Funciona en Linux, Windows, Mac, AWS, Azure, GCP... |

---

## Requisitos previos

- Docker instalado (v20.10+)
- Docker Compose instalado (v2.0+)
- Tu código de FastAPI (ya tienes)
- PostgreSQL (incluido en Docker)

---

## Instalación de Docker

### Linux (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt update

# Instalar Docker y Docker Compose
sudo apt install -y docker.io docker-compose

# Dar permisos a tu usuario (sin sudo)
sudo usermod -aG docker $USER
newgrp docker

# Iniciar Docker automáticamente
sudo systemctl enable docker
sudo systemctl start docker

# Verificar instalación
docker --version
docker-compose --version
```

### Alternativa: Snap (más rápido)

```bash
sudo snap install docker
sudo snap install docker-compose
```

### MacOS o Windows

Descargar [Docker Desktop](https://www.docker.com/products/docker-desktop) e instalar.

---

## Archivos creados

### 1. **requirements.txt** ✅
```
Contiene todas las dependencias de Python:
- FastAPI 0.129.0
- SQLAlchemy 2.0.46
- psycopg2-binary (para PostgreSQL)
- python-dotenv (para variables de entorno)
- Otros paquetes de autenticación y validación
```

Se genera con:
```bash
pip freeze > requirements.txt
```

---

### 2. **Dockerfile** ✅ (Imagen de tu app)

**Estrategia: Multi-stage build**

```dockerfile
# ETAPA 1: Builder (compila dependencias)
- Instala compilador (gcc)
- Instala todas las dependencias
- Pesa ~600MB

# ETAPA 2: Runtime (imagen final)
- Solo incluye lo necesario
- Copia packages compilados de ETAPA 1
- Pesa ~200MB (3x más ligera)
```

**Características importantes:**
- ✅ Usuario no-root por seguridad (appuser)
- ✅ Health check automático
- ✅ Expone puerto 8000
- ✅ Optimizado para producción

---

### 3. **docker-compose.yml** ✅ (Para DESARROLLO)

```yaml
version: '3.9'

Servicios:
  postgres: 
    - Imagen: postgres:16-alpine
    - Puerto: 5432
    - Variables: DB_USER, DB_PASSWORD, DB_NAME
    - Volumen: postgres_data (persiste datos)
    
  fastapi:
    - Build: ./Dockerfile
    - Puerto: 8000
    - Volumen: . (código local, para reload automático)
    - Command: uvicorn app:app --reload
```

**Para desarrollo con reload automático:**
```bash
docker-compose up
```

---

### 4. **docker-compose.prod.yml** ✅ (Para PRODUCCIÓN)

Diferencias importantes vs desarrollo:

| Aspecto | Desarrollo | Producción |
|---------|-----------|-----------|
| **Reload** | ✅ Sí (--reload) | ❌ No (más rápido) |
| **Volumen código** | ✅ Mapeado | ❌ No (copia estática) |
| **Restart** | unless-stopped | always |
| **Logs** | stdout | JSON files (rotados) |
| **recursos** | Sin límites | CPU 1, RAM 512M |

**Para producción:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

### 5. **.env** ✅ (Variables de entorno)

```env
DB_USER=postgres
DB_PASSWORD=postgres_local_dev
DB_HOST=postgres              # Nombre del servicio Docker
DB_PORT=5432
DB_NAME=nova_db
API_PORT=8000
```

**En servidor de producción, cambia:**
```env
DB_PASSWORD=TU_PASSWORD_SEGURO_AQUI
```

---

### 6. **.env.example** ✅ (Template)

Plantilla de ejemplo para que otros sepan qué variables necesitan:
```env
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=postgres
DB_PORT=5432
DB_NAME=nova_db
API_PORT=8000
```

Se sube a GitHub (sin contraseñas reales).

---

### 7. **.dockerignore** ✅ (Qué excluir)

Archivos que **NO** se copian a la imagen (reduce tamaño):
```
__pycache__/
venv/
.git/
.env (no incluye contraseñas)
*.md
.DS_Store
```

---

## Configuración explicada

### Networking en Docker

```
┌─────────────────────────┐
│  tu máquina (host)      │
│  ─────────────────────  │
│  localhost:8000   ──────┼─> puerto 8000 FastAPI
│  localhost:5432   ──────┼─> puerto 5432 PostgreSQL
└─────────────────────────┘
         ↑
         │ networks.nova_network (bridge)
         │
    ┌────┴─────────────────┐
    │                      │
    │   CONTENEDORES       │
    │                      │
    │ ┌──────────────────┐ │
    │ │ postgres:51432   │ │
    │ │ (interno)        │ │
    │ └──────────────────┘ │
    │                      │
    │ ┌──────────────────┐ │
    │ │ fastapi:8000     │ │
    │ │ conecta a        │ │
    │ │ "postgres:5432"  │ │
    │ └──────────────────┘ │
    │                      │
    └──────────────────────┘
```

**Por eso en `config/config.py` usamos:**
```python
DB_HOST = os.environ.get("DB_HOST")  # "postgres" (nombre del servicio)
```

### Volúmenes en Docker

```yaml
volumes:
  postgres_data: /var/lib/postgresql/data
  # Los datos persisten incluso si eliminas el contenedor
```

Si ejecutas `docker-compose down -v`, se eliminan todos los datos.

### Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')"
```

Comprueba que la app esté respondiendo cada 30 segundos.

---

## Cómo ejecutar

### Opción 1: DESARROLLO (con reload automático)

```bash
cd /home/sebas/NOVA/nova_back

# Construir imágenes (primera vez)
docker-compose build

# Levantar servicios
docker-compose up

# Verás logs en tiempo real
# Accede a: http://localhost:8000
# API docs: http://localhost:8000/docs
```

**Para detener:**
```bash
# En otra terminal o Ctrl+C
docker-compose down
```

---

### Opción 2: PRODUCCIÓN (sin reload, optimizado)

**Paso 1:** Editar `.env` con contraseña segura
```bash
nano .env
# Cambiar: DB_PASSWORD=tu_password_muy_seguro_aqui
```

**Paso 2:** Construir imágenes (si no lo hiciste)
```bash
docker-compose -f docker-compose.prod.yml build
```

**Paso 3:** Levantar en background
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Verificar estado:**
```bash
docker-compose -f docker-compose.prod.yml ps
```

---

### Opción 3: TODO EN UN COMANDO (recomendado para servidor)

```bash
cd /home/sebas/NOVA/nova_back && \
docker-compose -f docker-compose.prod.yml build && \
docker-compose -f docker-compose.prod.yml up -d && \
docker-compose -f docker-compose.prod.yml ps
```

O si ya construiste:

```bash
cd /home/sebas/NOVA/nova_back && docker-compose -f docker-compose.prod.yml up -d
```

---

## Comandos útiles

### Ver estado

```bash
# Ver contenedores en ejecución
docker-compose ps

# Ver estado detallado
docker-compose ps -a
```

### Logs

```bash
# Todos los logs en tiempo real
docker-compose logs -f

# Solo FastAPI
docker-compose logs -f fastapi

# Solo PostgreSQL
docker-compose logs -f postgres

# Últimas 50 líneas
docker-compose logs --tail=50
```

### Ejecutar comandos dentro del contenedor

```bash
# Bash en FastAPI
docker-compose exec fastapi bash

# Python en FastAPI
docker-compose exec fastapi python -c "import app; print('OK')"

# SQL en PostgreSQL
docker-compose exec postgres psql -U postgres -d nova_db -c "SELECT version();"

# Ver las bases de datos
docker-compose exec postgres psql -U postgres -l
```

### Limpiar

```bash
# Parar servicios (mantiene datos)
docker-compose down

# Parar y eliminar volúmenes (BORRA TODOS LOS DATOS)
docker-compose down -v

# Reconstruir sin caché
docker-compose build --no-cache

# Eliminar imágenes no usadas
docker image prune -a
```

### Actualizar código

```bash
# Si editaste config.py u otro archivo:
docker-compose restart fastapi

# O reconstruir si cambió requirements.txt:
docker-compose build && docker-compose up -d
```

---

## Troubleshooting

### ❌ "docker: command not found"

```bash
# Solución: Instalar Docker
sudo apt install docker.io
# O instalar desde Snap
sudo snap install docker
```

---

### ❌ "Permission denied while trying to connect to Docker daemon"

```bash
# Solución 1: Usar sudo
sudo docker-compose up

# Solución 2: Dar permisos al usuario (permanente)
sudo usermod -aG docker $USER
newgrp docker
```

---

### ❌ "port 5432 is already in use"

```bash
# Otra instancia usando ese puerto
# Solución 1: Usar otro puerto en .env
API_PORT=8001
DB_PORT=5433

# Solución 2: Matar el proceso anterior
sudo lsof -i :5432
sudo kill -9 <PID>

# Solución 3: Eliminar contenedores viejos
docker-compose down -v
```

---

### ❌ "fastapi service exited with code 1"

```bash
# Ver el error
docker-compose logs fastapi

# Probables causas:
# 1. requirements.txt incompleto → docker-compose build --no-cache
# 2. config.py con ruta incorrecta → ajustar imports
# 3. BD no disponible → esperar a que postgres esté healthy
```

---

### ❌ PostgreSQL no inicia

```bash
# Ver logs
docker-compose logs postgres

# Reconstruir volumen
docker-compose down -v
docker-compose up postgres
```

---

### ✅ Verificar que todo funciona

```bash
# Prueba 1: API responde
curl http://localhost:8000/

# Prueba 2: Acceder a documentación
# Abre en navegador: http://localhost:8000/docs

# Prueba 3: PostgreSQL responde
docker-compose exec postgres pg_isready -U postgres
```

---

## Deploy en Servidor de Producción

### Paso 1: Clonar repo en servidor

```bash
ssh usuario@servidor
cd /opt/
git clone https://github.com/tu_usuario/nova_back.git
cd nova_back
```

### Paso 2: Crear .env seguro

```bash
nano .env
```

Editarlo con:
```env
DB_USER=postgres
DB_PASSWORD=contraseña_super_segura_12345
DB_HOST=postgres
DB_PORT=5432
DB_NAME=nova_db
API_PORT=8000
```

### Paso 3: Levantar servicios

```bash
docker-compose -f docker-compose.prod.yml up -d
docker-compose ps
```

### Paso 4: Configurar Nginx (reverse proxy - OPCIONAL)

Si quieres acceder por `tu_dominio.com` en lugar de `IP:8000`:

```nginx
server {
    listen 80;
    server_name tu_dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Resumen Visual

```
┌─────────────────────────────────────────────────────────┐
│                    TU SERVIDOR                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  $ docker-compose -f docker-compose.prod.yml up -d    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │     DOCKER CONTAINER                            │  │
│  │                                                 │  │
│  │  ┌──────────────────┐   ┌─────────────────┐   │  │
│  │  │ PostgreSQL 16    │ ← │ FastAPI 0.129   │   │  │
│  │  │ puerto 5432      │   │ puerto 8000     │   │  │
│  │  │ nova_db          │   │ app.py          │   │  │
│  │  │ datos persistidos │   │ routers/        │   │  │
│  │  │ en volumen       │   │ models/         │   │  │
│  │  └──────────────────┘   │ schemas/        │   │  │
│  │                         └─────────────────┘   │  │
│  └──────────────────────────────────────────────┘  │
│                        ↑                            │
│                        │                            │
│          localhost:8000 (desde tu PC)              │
│      o  tu_servidor.com:8000 (desde web)           │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Checklist Final

- [x] `requirements.txt` creado
- [x] `Dockerfile` optimizado (multi-stage)
- [x] `docker-compose.yml` para desarrollo
- [x] `docker-compose.prod.yml` para producción
- [x] `.env` con variables locales
- [x] `.env.example` como template
- [x] `.dockerignore` para limpiar imagen
- [x] Docker instalado
- [x] Imágenes construidas (`docker-compose build`)
- [x] Servicios levantados (`docker-compose up -d`)

---

## Próximos pasos

1. **Prueba en desarrollo:**
   ```bash
   docker-compose up
   ```

2. **Prueba en producción:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Deploy en servidor real:**
   ```bash
   ssh usuario@servidor
   docker-compose -f docker-compose.prod.yml up -d
   ```

---

**¡Tu aplicación está lista para escalar! 🚀**
