from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from schemas.user_schema import (
    RecruiterRegistrationRequest,
    JobSeekerRegistrationRequest,
    LoginRequest,
    ProfileUpdateRequest,
    AuthResponse
)
from services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

user_service = UserService()

@router.post("/register/recruiter", response_model=AuthResponse)
async def register_recruiter(request: RecruiterRegistrationRequest):
    try:
        logger.info(f"Registering recruiter: {request.email}")
        
        result = await user_service.register_recruiter(request.dict())
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message="Recruiter registered successfully",
                user=result["user"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/register/job-seeker", response_model=AuthResponse)
async def register_job_seeker(request: JobSeekerRegistrationRequest):
    try:
        logger.info(f"Registering job seeker: {request.email}")
        
        result = await user_service.register_job_seeker(request.dict())
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message="Job seeker registered successfully",
                user=result["user"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    try:
        logger.info(f"Login attempt: {request.email}")
        
        result = await user_service.login(request.email, request.password)
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message="Login successful",
                user=result["user"]
            )
        else:
            raise HTTPException(status_code=401, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    try:
        user = await user_service.get_user(user_id)
        
        if user:
            return {"success": True, "user": user}
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile")

@router.put("/profile/{user_id}")
async def update_profile(user_id: str, request: ProfileUpdateRequest):
    try:
        update_data = request.dict(exclude_none=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        success = await user_service.update_profile(user_id, update_data)
        
        if success:
            return {"success": True, "message": "Profile updated"}
        else:
            raise HTTPException(status_code=400, detail="Update failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Update failed")

@router.post("/check-email")
async def check_email(email: str = Body(..., embed=True)):
    try:
        exists = await user_service.check_email_exists(email)
        return {"success": True, "available": not exists}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Check failed")