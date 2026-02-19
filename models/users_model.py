from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
user = Table("users", metadata, autoload_with=engine)
