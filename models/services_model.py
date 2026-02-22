from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
service_model = Table("services", metadata, autoload_with=engine)
