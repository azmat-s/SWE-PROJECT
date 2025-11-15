from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from services.matching_service import matching_service
from services.llm import get_llm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/llm", tags=["LLM"])

class MatchRequest(BaseModel):
    resume_data: Dict[str, Any] = Field(..., description="Resume information")
    job_data: Dict[str, Any] = Field(..., description="Job details")
    job_id: str = Field(..., description="Job ID")
    application_id: Optional[str] = Field(None, description="Application ID")

class SkillExtractionRequest(BaseModel):
    text: str = Field(..., description="Text to extract skills from")
    text_type: str = Field("resume", description="Type of text: resume or job_description")

class BulkMatchRequest(BaseModel):
    job_data: Dict[str, Any] = Field(..., description="Job details")
    job_id: str = Field(..., description="Job ID")
    candidates: List[Dict[str, Any]] = Field(..., description="List of candidate data")

@router.post("/match/calculate")
async def calculate_match(
    request: MatchRequest
):
    try:
        # Using a default user_id for now since no auth
        user_id = request.resume_data.get('user_id', 'default_user')
        
        match_result = await matching_service.calculate_match(
            resume_data=request.resume_data,
            job_data=request.job_data,
            user_id=user_id,
            job_id=request.job_id,
            application_id=request.application_id
        )
        
        return {
            "success": True,
            "data": match_result.dict(),
            "match_level": match_result.get_match_level()
        }
        
    except Exception as e:
        logger.error(f"Error calculating match: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match/result/{application_id}")
async def get_match_result(
    application_id: str
):
    try:
        result = await matching_service.get_match_result(application_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Match result not found")
        
        return {
            "success": True,
            "data": result.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving match result: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match/job/{job_id}/top")
async def get_top_candidates(
    job_id: str,
    limit: int = Query(10, ge=1, le=100)
):
    try:
        # No auth check for now
        results = await matching_service.get_top_matches_for_job(job_id, limit)
        
        return {
            "success": True,
            "data": [result.dict() for result in results],
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving top candidates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match/history")
async def get_match_history(
    user_id: str = Query(..., description="User ID to get history for"),
    limit: int = Query(20, ge=1, le=100)
):
    try:
        results = await matching_service.get_user_match_history(user_id, limit)
        
        return {
            "success": True,
            "data": [result.dict() for result in results],
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving match history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match/bulk")
async def bulk_match_candidates(
    request: BulkMatchRequest
):
    try:
        # No auth check for now
        results = await matching_service.bulk_match_candidates(
            job_data=request.job_data,
            job_id=request.job_id,
            candidates=request.candidates
        )
        
        return {
            "success": True,
            "data": [result.dict() for result in results],
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error in bulk matching: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract/skills")
async def extract_skills(
    request: SkillExtractionRequest
):
    try:
        llm_service = get_llm_service()
        skills = await llm_service.extract_skills(request.text)
        
        return {
            "success": True,
            "data": {
                "skills": skills,
                "count": len(skills)
            }
        }
        
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match/statistics/{job_id}")
async def get_job_statistics(
    job_id: str
):
    try:
        # No auth check for now
        stats = await matching_service.get_statistics_for_job(job_id)
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_available_providers():
    try:
        llm_service = get_llm_service()
        providers = llm_service.get_available_providers()
        
        return {
            "success": True,
            "data": {
                "providers": providers,
                "count": len(providers)
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cache/clear")
async def clear_cache():
    try:
        # No admin check for now
        llm_service = get_llm_service()
        llm_service.clear_cache()
        
        return {
            "success": True,
            "message": "Cache cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))