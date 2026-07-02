from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

# Routers
from app.auth import router as auth_router
from app.upload import router as upload_router
from app.profile import router as profile_router
from app.kpis import router as kpis_router
from app.charts import router as charts_router
from app.insights import router as insights_router
from app.ai import router as ai_router
from app.chatbot import router as chatbot_router
from app.forecast import router as forecast_router
from app.datasets import router as datasets_router

# Global Exception Handler
from app.exceptions import register_exception_handlers

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Business Analytics Platform",
    description="""
An AI-powered Business Analytics Platform.

## Features
- JWT Authentication
- CSV Dataset Upload
- Dataset Profiling
- KPI Dashboard
- Interactive Charts
- AI Business Insights (Gemini)
- Chat with Your Data
- Sales Forecasting (Prophet)
- MySQL Database
""",
    version="1.0.0"
)

# -------------------------------
# CORS Configuration
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Global Exception Handler
register_exception_handlers(app)

# -------------------------------
# Home
# -------------------------------

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to AI Business Analytics Platform",
        "status": "Running Successfully",
        "version": "1.0.0"
    }


# -------------------------------
# Health Check
# -------------------------------

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }


# -------------------------------
# Authentication
# -------------------------------

app.include_router(
    auth_router,
    tags=["Authentication"]
)

# -------------------------------
# Dataset
# -------------------------------

app.include_router(
    upload_router,
    tags=["Upload"]
)

app.include_router(
    profile_router,
    tags=["Dataset Profile"]
)

app.include_router(
    datasets_router,
    tags=["Datasets"]
)

# -------------------------------
# Analytics
# -------------------------------

app.include_router(
    kpis_router,
    tags=["KPIs"]
)

app.include_router(
    charts_router,
    tags=["Charts"]
)

app.include_router(
    insights_router,
    tags=["Insights"]
)

# -------------------------------
# AI
# -------------------------------

app.include_router(
    ai_router,
    tags=["AI Insights"]
)

app.include_router(
    chatbot_router,
    tags=["AI Chat"]
)

# -------------------------------
# Forecasting
# -------------------------------

app.include_router(
    forecast_router,
    tags=["Forecast"]
)