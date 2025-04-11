from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import functions
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Serverless Function Execution Platform",
    description="A platform for executing user-defined functions in isolated containers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(functions.router, prefix="/functions", tags=["functions"]) 