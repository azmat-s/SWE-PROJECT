import os
import asyncio
import aiohttp
from typing import Dict, Any, List
import json
import re
from services.llm.llm_service import LLMProviderInterface
import logging

logger = logging.getLogger(__name__)

class OpenRouterAdapter(LLMProviderInterface):
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv('APP_URL', 'http://localhost:8000'),
            "X-Title": "MatchWise",
            "Content-Type": "application/json"
        }
        self.session = None
        
    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
    async def _close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def is_available(self) -> bool:
        if not self.api_key:
            return False
            
        try:
            await self._ensure_session()
            async with self.session.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"OpenRouter availability check failed: {e}")
            return False
    
    async def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        await self._ensure_session()
        
        messages = self._create_analysis_messages(resume_text, job_description)
        
        try:
            async with self.session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 800,
                    "top_p": 0.9
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                return self._parse_analysis_response(content)
                
        except aiohttp.ClientError as e:
            logger.error(f"OpenRouter API error: {e}")
            if hasattr(e, 'status') and e.status == 429:
                await asyncio.sleep(10)
                return await self.analyze_match(resume_text, job_description)
            raise
        except Exception as e:
            logger.error(f"OpenRouter analysis failed: {e}")
            raise
    
    async def extract_skills(self, text: str) -> List[str]:
        await self._ensure_session()
        
        messages = [
            {
                "role": "system",
                "content": "You are a skills extraction expert. Extract only technical and professional skills."
            },
            {
                "role": "user",
                "content": f"""Extract all technical and professional skills from this text.
                Return ONLY a comma-separated list of skills, nothing else.
                
                Text: {text[:2000]}
                
                Skills:"""
            }
        ]
        
        try:
            async with self.session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 300
                },
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                skills = [s.strip() for s in content.split(',') if s.strip()]
                return skills[:25]
                
        except Exception as e:
            logger.error(f"Skill extraction failed: {e}")
            return []
    
    def _create_analysis_messages(self, resume_text: str, job_description: str) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": """You are an expert ATS and job matching system. Analyze resumes against job descriptions.
                Always respond with valid JSON containing these exact fields:
                - overall_score (0-100)
                - matched_skills (array)
                - skill_gaps (array)
                - transferable_skills (array)
                - experience_match (0-100)
                - education_match (0-100)
                - recommendations (array)"""
            },
            {
                "role": "user",
                "content": f"""Analyze this resume against the job description and provide a detailed match analysis.
                
                Job Description:
                {job_description[:2000]}
                
                Resume:
                {resume_text[:2000]}
                
                Provide your analysis as a JSON object with the specified fields."""
            }
        ]
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                
                parsed['overall_score'] = min(100, max(0, int(parsed.get('overall_score', 0))))
                parsed['experience_match'] = min(100, max(0, int(parsed.get('experience_match', 0))))
                parsed['education_match'] = min(100, max(0, int(parsed.get('education_match', 0))))
                
                for field in ['matched_skills', 'skill_gaps', 'transferable_skills', 'recommendations']:
                    if field not in parsed or not isinstance(parsed[field], list):
                        parsed[field] = []
                
                return parsed
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
        
        default_response = {
            "overall_score": 50,
            "matched_skills": [],
            "skill_gaps": [],
            "transferable_skills": [],
            "experience_match": 50,
            "education_match": 50,
            "recommendations": ["Unable to perform detailed analysis"]
        }
        
        try:
            lines = response_text.split('\n')
            for line in lines:
                if 'score' in line.lower():
                    score_match = re.search(r'(\d+)', line)
                    if score_match:
                        default_response["overall_score"] = min(100, int(score_match.group(1)))
                        break
            
            keyword_scores = {
                "perfect": 95, "excellent": 90, "strong": 80, "good": 70,
                "moderate": 60, "fair": 50, "weak": 30, "poor": 20
            }
            
            response_lower = response_text.lower()
            for keyword, score in keyword_scores.items():
                if keyword in response_lower:
                    default_response["overall_score"] = score
                    break
                    
        except Exception as e:
            logger.error(f"Error in fallback parsing: {e}")
        
        return default_response
    
    def __del__(self):
        if self.session and not self.session.closed:
            asyncio.create_task(self._close_session())