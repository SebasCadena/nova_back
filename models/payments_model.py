from sqlalchemy import Table
from config.config import metadata, engine

#Importar ya existentes
payment_model = Table("payments", metadata, autoload_with=engine)