from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

metadata = MetaData()

# Función para obtener una conexión (mejor práctica para PostgreSQL)
def get_connection():
    conn = engine.connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

print(f"✅ Conectado a la base de datos: {DB_NAME} en {DB_HOST}:{DB_PORT}")