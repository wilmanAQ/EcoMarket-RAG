"""
Configuration Settings Module
Centralized configuration using pydantic-settings
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "EcoMarket RAG"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    llm_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-3-small"
    
    # Vector Store
    vector_store_path: str = "./data/vectorstore"
    collection_name: str = "ecomarket_docs"
    
    # RAG Parameters
    top_k_documents: int = 3
    max_context_length: int = 4000
    temperature: float = 0.7
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "logs/ecomarket_rag.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
