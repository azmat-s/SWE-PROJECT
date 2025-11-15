from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
import hashlib
import secrets

class User(BaseModel):
    user_id: Optional[str] = Field(alias="_id", default=None)
    email: str
    password: str  # This will store the hashed password
    name: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                           password.encode('utf-8'), 
                                           salt.encode('utf-8'), 
                                           100000)
        return f"{salt}${password_hash.hex()}"
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            salt, hash_value = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256',
                                          password.encode('utf-8'),
                                          salt.encode('utf-8'),
                                          100000)
            return new_hash.hex() == hash_value
        except:
            return False
    
    def login(self) -> bool:
        # Placeholder for login logic
        return True
    
    def logout(self) -> None:
        # Placeholder for logout logic
        pass
    
    def update_profile(self) -> None:
        # Placeholder for profile update logic
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        data = self.dict(by_alias=True)
        if "_id" in data and data["_id"]:
            data["_id"] = ObjectId(data["_id"])
        return data
    
    @classmethod
    def from_mongo(cls, data: Dict[str, Any]):
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)

class Recruiter(User):
    company: str
    designation: Optional[str] = None
    
    def post_job(self, job: Dict[str, Any]) -> None:
        pass
    
    def update_job(self, job_id: str, job: Dict[str, Any]) -> None:
        pass
    
    def delete_job(self, job_id: str) -> None:
        pass
    
    def view_previous_jobs(self) -> List[Dict]:
        return []
    
    def select_job(self, job_id: str) -> Dict:
        return {}
    
    def view_top_candidates(self, job_id: str) -> List[Dict]:
        return []
    
    def get_ranked_candidates(self, job_id: str) -> List[Dict]:
        return []
    
    def add_notes(self, application_id: str, note: str) -> None:
        pass
    
    def chat_with_candidate(self, candidate_id: str) -> None:
        pass

class JobSeeker(User):
    skills: List[str] = Field(default_factory=list)
    experience: Optional[str] = None
    education: Optional[str] = None
    resume_url: Optional[str] = None
    resume_text: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    def search_jobs(self, keywords: str) -> List[Dict]:
        return []
    
    def apply_to_job(self, job_id: str) -> None:
        pass
    
    def track_application(self, application_id: str) -> Dict:
        return {}
    
    def view_match_score(self, job_id: str) -> float:
        return 0.0
    
    def view_preference_match_score(self, job_id: str) -> float:
        return 0.0
    
    def upload_resume(self, file: Any) -> None:
        pass