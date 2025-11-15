from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from services.llm.matching_strategy import LLMMatchingStrategy
from models.match_result import MatchResult
from app.database import get_database
from bson import ObjectId

logger = logging.getLogger(__name__)

class MatchingService:
    def __init__(self):
        self.strategy = LLMMatchingStrategy()
        self.db = None
        
    async def _get_db(self):
        if self.db is None:
            self.db = await get_database()
        return self.db
    
    async def calculate_match(
        self, 
        resume_data: Dict[str, Any], 
        job_data: Dict[str, Any],
        user_id: str,
        job_id: str,
        application_id: Optional[str] = None
    ) -> MatchResult:
        try:
            logger.info(f"Calculating match for user {user_id} and job {job_id}")
            
            match_data = await self.strategy.calculate_match(resume_data, job_data)
            
            match_result = MatchResult(
                application_id=application_id or str(ObjectId()),
                job_id=job_id,
                user_id=user_id,
                **match_data
            )
            
            db = await self._get_db()
            await self._save_match_result(db, match_result)
            
            logger.info(f"Match calculated successfully. Score: {match_result.overall_score}")
            return match_result
            
        except Exception as e:
            logger.error(f"Error calculating match: {e}")
            raise
    
    async def _save_match_result(self, db, match_result: MatchResult):
        try:
            collection = db.match_results
            result_dict = match_result.to_dict()
            
            if "_id" in result_dict and result_dict["_id"]:
                await collection.replace_one(
                    {"_id": result_dict["_id"]},
                    result_dict,
                    upsert=True
                )
            else:
                result = await collection.insert_one(result_dict)
                match_result.id = str(result.inserted_id)
                
        except Exception as e:
            logger.error(f"Error saving match result: {e}")
    
    async def get_match_result(self, application_id: str) -> Optional[MatchResult]:
        try:
            db = await self._get_db()
            collection = db.match_results
            
            result = await collection.find_one({"application_id": application_id})
            if result:
                return MatchResult.from_mongo(result)
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving match result: {e}")
            return None
    
    async def get_top_matches_for_job(
        self, 
        job_id: str, 
        limit: int = 10
    ) -> List[MatchResult]:
        try:
            db = await self._get_db()
            collection = db.match_results
            
            cursor = collection.find({"job_id": job_id}).sort("overall_score", -1).limit(limit)
            results = []
            async for doc in cursor:
                results.append(MatchResult.from_mongo(doc))
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving top matches: {e}")
            return []
    
    async def get_user_match_history(
        self, 
        user_id: str, 
        limit: int = 20
    ) -> List[MatchResult]:
        try:
            db = await self._get_db()
            collection = db.match_results
            
            cursor = collection.find({"user_id": user_id}).sort("calculated_at", -1).limit(limit)
            results = []
            async for doc in cursor:
                results.append(MatchResult.from_mongo(doc))
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving user match history: {e}")
            return []
    
    async def bulk_match_candidates(
        self, 
        job_data: Dict[str, Any],
        job_id: str,
        candidates: List[Dict[str, Any]]
    ) -> List[MatchResult]:
        results = []
        
        for candidate in candidates:
            try:
                resume_data = candidate.get('resume_data', {})
                user_id = candidate.get('user_id')
                application_id = candidate.get('application_id')
                
                match_result = await self.calculate_match(
                    resume_data, 
                    job_data, 
                    user_id, 
                    job_id, 
                    application_id
                )
                results.append(match_result)
                
            except Exception as e:
                logger.error(f"Error processing candidate {candidate.get('user_id')}: {e}")
                continue
        
        return sorted(results, key=lambda x: x.overall_score, reverse=True)
    
    async def update_match_result(
        self,
        application_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        try:
            db = await self._get_db()
            collection = db.match_results
            
            updates['updated_at'] = datetime.utcnow()
            
            result = await collection.update_one(
                {"application_id": application_id},
                {"$set": updates}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating match result: {e}")
            return False
    
    async def get_statistics_for_job(self, job_id: str) -> Dict[str, Any]:
        try:
            db = await self._get_db()
            collection = db.match_results
            
            pipeline = [
                {"$match": {"job_id": job_id}},
                {
                    "$group": {
                        "_id": None,
                        "total_applications": {"$sum": 1},
                        "average_score": {"$avg": "$overall_score"},
                        "max_score": {"$max": "$overall_score"},
                        "min_score": {"$min": "$overall_score"},
                        "excellent_matches": {
                            "$sum": {"$cond": [{"$gte": ["$overall_score", 85]}, 1, 0]}
                        },
                        "good_matches": {
                            "$sum": {"$cond": [
                                {"$and": [
                                    {"$gte": ["$overall_score", 70]},
                                    {"$lt": ["$overall_score", 85]}
                                ]}, 1, 0
                            ]}
                        }
                    }
                }
            ]
            
            result = await collection.aggregate(pipeline).to_list(1)
            
            if result:
                stats = result[0]
                del stats['_id']
                return stats
            
            return {
                "total_applications": 0,
                "average_score": 0,
                "max_score": 0,
                "min_score": 0,
                "excellent_matches": 0,
                "good_matches": 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

matching_service = MatchingService()
