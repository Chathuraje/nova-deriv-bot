from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.main import router as main_router

app = FastAPI()

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

