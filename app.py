from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.categories_router import category_router
from routers.services_router import service_router
from routers.products_router import product_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # agrega tus dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # o lista explícita incluyendo ngrok-skip-browser-warning
)

app.include_router(service_router)
app.include_router(category_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API julian"}