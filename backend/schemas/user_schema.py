from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    RECRUITER = "recruiter"
    JOB_SEEKER = "job_seeker"

# Registration Request Schemas (matching UI forms)
class RecruiterRegistrationRequest(BaseModel):
    full_name: str = Field(..., min_length=2, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    company_name: str = Field(..., min_length=2, description="Company name")
    company_website: Optional[str] = Field(None, description="Company website URL")
    password: str = Field(..., min_length=6, description="Password")
    confirm_password: str = Field(..., min_length=6, description="Confirm password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class JobSeekerRegistrationRequest(BaseModel):
    full_name: str = Field(..., min_length=2, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    resume_pdf: Optional[str] = Field(None, description="Resume PDF base64 or URL")
    password: str = Field(..., min_length=6, description="Password")
    confirm_password: str = Field(..., min_length=6, description="Confirm password")
    
    # Additional optional fields not shown in UI but useful
    skills: Optional[List[str]] = Field(default_factory=list)
    experience: Optional[str] = None
    education: Optional[str] = None
    resume_text: Optional[str] = None
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")

class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2)
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    designation: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    resume_url: Optional[str] = None
    resume_text: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

# Response Schemas
class BaseUserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    phone: Optional[str] = None
    created_at: datetime
    
class RecruiterResponse(BaseUserResponse):
    role: str = "recruiter"
    company: str
    designation: Optional[str] = None
    company_website: Optional[str] = None

class JobSeekerResponse(BaseUserResponse):
    role: str = "job_seeker"
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None
    resume_url: Optional[str] = None
    preferences: Dict[str, Any] = {}

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[Dict[str, Any]] = None
    token: Optional[str] = None