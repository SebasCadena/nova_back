from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
category_model = Table("categories", metadata, autoload_with=engine)
