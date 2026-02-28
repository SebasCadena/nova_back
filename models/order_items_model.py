from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
order_items_model = Table("order_items", metadata, autoload_with=engine)