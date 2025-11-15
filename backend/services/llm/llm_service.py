# services/llm/llm_service.py
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import json
import logging
from datetime import datetime, timedelta
import hashlib
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    HUGGINGFACE = "huggingface"
    OPENROUTER = "openrouter"

class LLMProviderInterface(ABC):
    @abstractmethod
    async def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def extract_skills(self, text: str) -> List[str]:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass

class LLMService:
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._providers: Dict[LLMProvider, LLMProviderInterface] = {}
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = timedelta(hours=24)
        self._primary_provider = LLMProvider.HUGGINGFACE
        self._initialized = True
        
    def register_provider(self, provider_type: LLMProvider, provider: LLMProviderInterface):
        self._providers[provider_type] = provider
        logger.info(f"Registered LLM provider: {provider_type.value}")
    
    def _get_cache_key(self, resume_text: str, job_description: str) -> str:
        content = f"{resume_text}:{job_description}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        if 'timestamp' not in cache_entry:
            return False
        cache_time = datetime.fromisoformat(cache_entry['timestamp'])
        return datetime.now() - cache_time < self._cache_ttl
    
    async def analyze_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        cache_key = self._get_cache_key(resume_text, job_description)
        
        if cache_key in self._cache and self._is_cache_valid(self._cache[cache_key]):
            logger.info("Returning cached match result")
            return self._cache[cache_key]['data']
        
        async with self._lock:
            primary_provider = self._providers.get(self._primary_provider)
            if primary_provider and await primary_provider.is_available():
                try:
                    result = await primary_provider.analyze_match(resume_text, job_description)
                    self._cache[cache_key] = {
                        'data': result,
                        'timestamp': datetime.now().isoformat()
                    }
                    return result
                except Exception as e:
                    logger.error(f"Primary provider {self._primary_provider.value} failed: {e}")
            
            for provider_type, provider in self._providers.items():
                if provider_type == self._primary_provider:
                    continue
                    
                try:
                    if await provider.is_available():
                        result = await provider.analyze_match(resume_text, job_description)
                        self._cache[cache_key] = {
                            'data': result,
                            'timestamp': datetime.now().isoformat()
                        }
                        logger.info(f"Used fallback provider: {provider_type.value}")
                        return result
                except Exception as e:
                    logger.error(f"Provider {provider_type.value} failed: {e}")
                    continue
            
            raise Exception("All LLM providers are unavailable")
    
    async def extract_skills(self, text: str) -> List[str]:
        for provider_type, provider in self._providers.items():
            try:
                if await provider.is_available():
                    return await provider.extract_skills(text)
            except Exception as e:
                logger.error(f"Provider {provider_type.value} failed for skill extraction: {e}")
                continue
        
        return []
    
    async def calculate_match_score(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        try:
            analysis = await self.analyze_match(resume_text, job_description)
            
            match_score = analysis.get('overall_score', 0)
            skill_gaps = analysis.get('skill_gaps', [])
            transferable_skills = analysis.get('transferable_skills', [])
            recommendations = analysis.get('recommendations', [])
            
            return {
                'match_score': match_score,
                'skill_gaps': skill_gaps,
                'transferable_skills': transferable_skills,
                'recommendations': recommendations,
                'analysis': analysis
            }
        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            return {
                'match_score': 0,
                'skill_gaps': [],
                'transferable_skills': [],
                'recommendations': [],
                'error': str(e)
            }
    
    def clear_cache(self):
        self._cache.clear()
        logger.info("LLM cache cleared")
    
    def get_available_providers(self) -> List[str]:
        return [provider.value for provider in self._providers.keys()]