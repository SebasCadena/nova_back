from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
carrito_model = Table("cart", metadata, autoload_with=engine)