from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
cart_items_model = Table("cart_items", metadata, autoload_with=engine)