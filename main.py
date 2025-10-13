#!/usr/bin/env python3
"""
EcoMarket RAG Solution - Main Entry Point
FastAPI application for RAG-based product queries and recommendations
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

from app.rag.embeddings import EmbeddingService
from app.rag.retriever import DocumentRetriever
from app.rag.generator import ResponseGenerator
from app.config.settings import get_settings
# Setup logging
logger.info("Logging initialized")

# Global instances
embedding_service = None
retriever = None
generator = None


class QueryRequest(BaseModel):
    """Request model for RAG queries"""
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    """Response model for RAG queries"""
    answer: str
    sources: list[dict]
    confidence: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global embedding_service, retriever, generator
    
    logger.info("Initializing EcoMarket RAG application...")
    settings = get_settings()
    
    # Initialize services
    embedding_service = EmbeddingService()
    retriever = DocumentRetriever(embedding_service)
    generator = ResponseGenerator()
    
    logger.info("Application initialized successfully")
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(
    title="EcoMarket RAG API",
    description="RAG-based product information and recommendation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "EcoMarket RAG API"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "embedding_service": embedding_service is not None,
        "retriever": retriever is not None,
        "generator": generator is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Process RAG query"""
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Retrieve relevant documents
        documents = await retriever.retrieve(
            request.query,
            top_k=request.top_k
        )
        
        # Generate response
        response = await generator.generate(
            query=request.query,
            documents=documents,
            temperature=request.temperature
        )
        
        return QueryResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
