"""
FastAPI application entry point.
Main application setup with middleware, CORS, and route registration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.translate import router as translate_router
from config import settings
from utils.logging import setup_logging, get_logger

# Setup logging
setup_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting AI Translation Assistant API")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"LLM Model: {settings.llm_model}")
    yield
    logger.info("Shutting down AI Translation Assistant API")


# Create FastAPI app
app = FastAPI(
    title="AI Translation Assistant",
    description="Translate Chinese to English with keyword extraction using LLM",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(translate_router, prefix="/api", tags=["Translation"])


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "service": "AI Translation Assistant",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
    )
