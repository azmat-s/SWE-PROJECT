# services/llm/__init__.py
import os
from services.llm.llm_service import LLMService, LLMProvider
from services.llm.huggingface_adapter import HuggingFaceAdapter
from services.llm.openrouter_adapter import OpenRouterAdapter
import logging

logger = logging.getLogger(__name__)

def initialize_llm_service() -> LLMService:
    llm_service = LLMService()
    
    providers_initialized = 0
    
    if os.getenv('HUGGINGFACE_API_KEY'):
        try:
            hf_adapter = HuggingFaceAdapter()
            llm_service.register_provider(LLMProvider.HUGGINGFACE, hf_adapter)
            providers_initialized += 1
            logger.info("HuggingFace provider initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize HuggingFace provider: {e}")
    else:
        logger.warning("HuggingFace API key not found")
    
    if os.getenv('OPENROUTER_API_KEY'):
        try:
            or_adapter = OpenRouterAdapter()
            llm_service.register_provider(LLMProvider.OPENROUTER, or_adapter)
            providers_initialized += 1
            logger.info("OpenRouter provider initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter provider: {e}")
    else:
        logger.warning("OpenRouter API key not found")
    
    if providers_initialized == 0:
        logger.error("No LLM providers were initialized. Please check your API keys.")
        raise ValueError("At least one LLM provider must be configured")
    
    logger.info(f"LLM Service initialized with {providers_initialized} provider(s)")
    return llm_service

def get_llm_service() -> LLMService:
    return LLMService()

__all__ = ['initialize_llm_service', 'get_llm_service', 'LLMService', 'LLMProvider']