# services/llm/huggingface_adapter.py
import os
import asyncio
import aiohttp
from typing import Dict, Any, List
import json
import re
from services.llm.llm_service import LLMProviderInterface
import logging

logger = logging.getLogger(__name__)

class HuggingFaceAdapter(LLMProviderInterface):
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model_name = os.getenv('HUGGINGFACE_MODEL', 'microsoft/Phi-3-mini-4k-instruct')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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
            async with self.session.post(
                f"{self.base_url}/{self.model_name}",
                headers=self.headers,
                json={"inputs": "test"},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status in [200, 503]
        except Exception as e:
            logger.error(f"HuggingFace availability check failed: {e}")
            return False
    
    async def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        await self._ensure_session()
        
        prompt = self._create_analysis_prompt(resume_text, job_description)
        
        try:
            async with self.session.post(
                f"{self.base_url}/{self.model_name}",
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 500,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 503:
                    await asyncio.sleep(5)
                    return await self.analyze_match(resume_text, job_description)
                
                response.raise_for_status()
                result = await response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                else:
                    generated_text = str(result)
                
                return self._parse_analysis_response(generated_text)
                
        except Exception as e:
            logger.error(f"HuggingFace analysis failed: {e}")
            raise
    
    async def extract_skills(self, text: str) -> List[str]:
        await self._ensure_session()
        
        prompt = f"""Extract technical and professional skills from this text.
        Return only a comma-separated list of skills.
        
        Text: {text[:1500]}
        
        Skills:"""
        
        try:
            async with self.session.post(
                f"{self.base_url}/{self.model_name}",
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "temperature": 0.2
                    }
                },
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    skills_text = result[0].get('generated_text', '')
                else:
                    skills_text = str(result)
                
                skills_text = skills_text.replace(prompt, '').strip()
                skills = [s.strip() for s in skills_text.split(',') if s.strip()]
                return skills[:20]
                
        except Exception as e:
            logger.error(f"Skill extraction failed: {e}")
            return []
    
    def _create_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        return f"""Analyze the match between this resume and job description.
        Provide a JSON response with the following structure:
        {{
            "overall_score": <0-100>,
            "matched_skills": ["skill1", "skill2"],
            "skill_gaps": ["missing_skill1", "missing_skill2"],
            "transferable_skills": ["skill1", "skill2"],
            "experience_match": <0-100>,
            "education_match": <0-100>,
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        
        Job Description:
        {job_description[:1500]}
        
        Resume:
        {resume_text[:1500]}
        
        Analysis:"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        default_response = {
            "overall_score": 0,
            "matched_skills": [],
            "skill_gaps": [],
            "transferable_skills": [],
            "experience_match": 0,
            "education_match": 0,
            "recommendations": []
        }
        
        try:
            score_match = re.search(r'score[:\s]*(\d+)', response_text, re.IGNORECASE)
            if score_match:
                default_response["overall_score"] = min(100, int(score_match.group(1)))
            
            if "high match" in response_text.lower():
                default_response["overall_score"] = max(75, default_response["overall_score"])
            elif "moderate match" in response_text.lower():
                default_response["overall_score"] = max(50, default_response["overall_score"])
            elif "low match" in response_text.lower():
                default_response["overall_score"] = min(40, default_response["overall_score"])
                
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
        
        return default_response
    
    def __del__(self):
        if self.session and not self.session.closed:
            asyncio.create_task(self._close_session())