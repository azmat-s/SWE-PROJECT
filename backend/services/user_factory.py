from typing import Dict, Any, Union
from models.user import User, Recruiter, JobSeeker
import logging

logger = logging.getLogger(__name__)

class UserFactory:
    
    @staticmethod
    def create_user(user_type: str, data: Dict[str, Any]) -> Union[Recruiter, JobSeeker]:
        if user_type == "recruiter":
            return UserFactory.create_recruiter(data)
        elif user_type == "job_seeker":
            return UserFactory.create_job_seeker(data)
        else:
            raise ValueError(f"Invalid user type: {user_type}")
    
    @staticmethod
    def create_recruiter(data: Dict[str, Any]) -> Recruiter:
        recruiter_data = {
            'email': data['email'],
            'password': data['password_hash'],
            'name': data['full_name'],
            'phone': data.get('phone'),
            'company': data['company_name'],
            'designation': data.get('designation')
        }
        return Recruiter(**recruiter_data)
    
    @staticmethod
    def create_job_seeker(data: Dict[str, Any]) -> JobSeeker:
        job_seeker_data = {
            'email': data['email'],
            'password': data['password_hash'],
            'name': data['full_name'],
            'phone': data.get('phone'),
            'skills': data.get('skills', []),
            'experience': data.get('experience'),
            'education': data.get('education'),
            'resume_url': data.get('resume_url'),
            'resume_text': data.get('resume_text'),
            'preferences': data.get('preferences', {})
        }
        return JobSeeker(**job_seeker_data)
    
    @staticmethod
    def create_from_mongo(data: Dict[str, Any]) -> Union[Recruiter, JobSeeker]:
        if 'company' in data:
            return Recruiter.from_mongo(data)
        else:
            return JobSeeker.from_mongo(data)