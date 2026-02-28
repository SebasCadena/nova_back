from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
order_model = Table("orders", metadata, autoload_with=engine)