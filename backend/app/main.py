# app/main.py
from fastapi import FastAPI
from services.llm import initialize_llm_service
from controllers.llm_controller import router as llm_router

app = FastAPI(title="MatchWise")

@app.on_event("startup")
async def startup_event():
    initialize_llm_service()
    
app.include_router(llm_router)# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.llm import initialize_llm_service
from controllers.llm_controller import router as llm_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MatchWise", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        initialize_llm_service()
        print("LLM Service initialized successfully")
    except Exception as e:
        print(f"Warning: LLM Service initialization failed: {e}")

app.include_router(llm_router)

@app.get("/")
async def root():
    return {"message": "MatchWise API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ci-cd-check")
async def ci_cd_check():
    return {"status": "CI/CD pipeline is operational"}