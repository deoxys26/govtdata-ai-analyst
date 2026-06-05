from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health_router import router as health_router
from app.routers.analytics_router import router as analytics_router
from app.routers.chat_router import router as chat_router


app = FastAPI(
    title="GovData AI Analyst",
    description="AI-powered analytics platform for government air quality data",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(analytics_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to GovData AI Analyst API"
    }
