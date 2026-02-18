from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
category = Table("categories", metadata, autoload_with=engine)
