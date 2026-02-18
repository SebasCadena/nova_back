from fastapi import FastAPI

from routers.categories_router import category_router
from routers.services_router import service_router
from routers.products_router import product_router

app = FastAPI()
app.include_router(service_router)
app.include_router(category_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API julian"}