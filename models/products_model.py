from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
product = Table("products", metadata, autoload_with=engine)
