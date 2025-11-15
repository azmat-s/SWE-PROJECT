from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class MatchResult(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    application_id: str
    job_id: str
    user_id: str
    overall_score: int = Field(ge=0, le=100)
    matched_skills: List[str] = []
    skill_gaps: List[str] = []
    transferable_skills: List[str] = []
    experience_match: int = Field(ge=0, le=100)
    education_match: int = Field(ge=0, le=100)
    location_match: int = Field(ge=0, le=100)
    recommendations: List[str] = []
    scoring_breakdown: Dict[str, Any] = {}
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    provider_used: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        
    def to_dict(self) -> Dict[str, Any]:
        data = self.dict(by_alias=True, exclude_none=True)
        if "_id" in data and data["_id"]:
            data["_id"] = ObjectId(data["_id"])
        return data
    
    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> "MatchResult":
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)
    
    def get_match_level(self) -> str:
        if self.overall_score >= 85:
            return "Excellent Match"
        elif self.overall_score >= 70:
            return "Good Match"
        elif self.overall_score >= 50:
            return "Fair Match"
        else:
            return "Low Match"
    
    def get_top_recommendations(self, limit: int = 3) -> List[str]:
        return self.recommendations[:limit] if self.recommendations else []
    
    def get_skill_match_percentage(self) -> float:
        total_skills = len(self.matched_skills) + len(self.skill_gaps)
        if total_skills == 0:
            return 0.0
        return (len(self.matched_skills) / total_skills) * 100