from typing import Optional, Dict, Any, Union
from datetime import datetime
from bson import ObjectId
import logging
from models.user import User, Recruiter, JobSeeker
from services.user_factory import UserFactory
from app.database import get_database

logger = logging.getLogger(__name__)

class UserService:
    
    def __init__(self):
        self.db = None
    
    async def _get_db(self):
        if self.db is None:
            self.db = await get_database()
        return self.db
    
    async def register_recruiter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            db = await self._get_db()
            
            # Check if email exists
            existing = await db.users.find_one({"email": data['email']})
            if existing:
                return {"success": False, "error": "Email already registered"}
            
            # Hash password
            password_hash = User.hash_password(data['password'])
            
            # Prepare recruiter data
            recruiter_data = {
                'email': data['email'],
                'password': password_hash,
                'name': data['full_name'],
                'phone': data.get('phone'),
                'company': data['company_name'],
                'designation': data.get('designation'),
                'created_at': datetime.utcnow()
            }
            
            if data.get('company_website'):
                recruiter_data['company_website'] = data['company_website']
            
            # Insert into database
            result = await db.users.insert_one(recruiter_data)
            
            return {
                "success": True,
                "user": {
                    "user_id": str(result.inserted_id),
                    "email": recruiter_data['email'],
                    "name": recruiter_data['name'],
                    "company": recruiter_data['company'],
                    "role": "recruiter"
                }
            }
            
        except Exception as e:
            logger.error(f"Error registering recruiter: {e}")
            return {"success": False, "error": str(e)}
    
    async def register_job_seeker(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            db = await self._get_db()
            
            # Check if email exists
            existing = await db.users.find_one({"email": data['email']})
            if existing:
                return {"success": False, "error": "Email already registered"}
            
            # Hash password
            password_hash = User.hash_password(data['password'])
            
            # Prepare job seeker data
            job_seeker_data = {
                'email': data['email'],
                'password': password_hash,
                'name': data['full_name'],
                'phone': data.get('phone'),
                'skills': data.get('skills', []),
                'experience': data.get('experience'),
                'education': data.get('education'),
                'resume_url': data.get('resume_pdf'),
                'resume_text': data.get('resume_text'),
                'preferences': data.get('preferences', {}),
                'created_at': datetime.utcnow()
            }
            
            # Insert into database
            result = await db.users.insert_one(job_seeker_data)
            
            return {
                "success": True,
                "user": {
                    "user_id": str(result.inserted_id),
                    "email": job_seeker_data['email'],
                    "name": job_seeker_data['name'],
                    "skills": job_seeker_data['skills'],
                    "role": "job_seeker"
                }
            }
            
        except Exception as e:
            logger.error(f"Error registering job seeker: {e}")
            return {"success": False, "error": str(e)}
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            db = await self._get_db()
            
            # Find user
            user_data = await db.users.find_one({"email": email})
            
            if not user_data:
                return {"success": False, "error": "Invalid email or password"}
            
            # Verify password
            if not User.verify_password(password, user_data['password']):
                return {"success": False, "error": "Invalid email or password"}
            
            # Determine user type
            is_recruiter = 'company' in user_data
            
            # Prepare response
            user_response = {
                "user_id": str(user_data['_id']),
                "email": user_data['email'],
                "name": user_data['name'],
                "role": "recruiter" if is_recruiter else "job_seeker"
            }
            
            if is_recruiter:
                user_response["company"] = user_data['company']
                user_response["designation"] = user_data.get('designation')
            else:
                user_response["skills"] = user_data.get('skills', [])
                user_response["experience"] = user_data.get('experience')
            
            return {"success": True, "user": user_response}
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {"success": False, "error": "Login failed"}
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            db = await self._get_db()
            user_data = await db.users.find_one({"_id": ObjectId(user_id)})
            
            if user_data:
                user_data['_id'] = str(user_data['_id'])
                user_data.pop('password', None)
                return user_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    async def update_profile(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        try:
            db = await self._get_db()
            
            # Remove sensitive fields
            update_data.pop('password', None)
            update_data.pop('_id', None)
            update_data.pop('email', None)  # Email shouldn't be changed without verification
            
            result = await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return False
    
    async def check_email_exists(self, email: str) -> bool:
        try:
            db = await self._get_db()
            count = await db.users.count_documents({"email": email})
            return count > 0
        except Exception as e:
            logger.error(f"Error checking email: {e}")
            return False