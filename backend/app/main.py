from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MatchWise API...")
    
    try:
        from services.llm import initialize_llm_service
        if os.getenv('HUGGINGFACE_API_KEY') or os.getenv('OPENROUTER_API_KEY'):
            initialize_llm_service()
            logger.info("LLM Service initialized")
        else:
            logger.warning("No LLM API keys found. LLM features will be disabled.")
    except Exception as e:
        logger.error(f"Failed to initialize LLM service: {e}")
    
    logger.info("MatchWise API started successfully")
    
    yield
    
    logger.info("Shutting down MatchWise API...")

app = FastAPI(
    title="MatchWise API",
    description="AI-powered job matching platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.auth_controller import router as auth_router
from controllers.llm_controller import router as llm_router

app.include_router(auth_router)
app.include_router(llm_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to MatchWise API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "MatchWise API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )