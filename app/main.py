from fastapi import FastAPI
from app.api.routers.main import router as main_router

app = FastAPI()

app.include_router(main_router)

