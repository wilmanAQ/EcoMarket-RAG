"""
Response Generator Module
Generates responses using LLM based on retrieved documents
"""

import openai
from typing import List, Dict, Any
from loguru import logger
from app.config.settings import get_settings


class ResponseGenerator:
    """
    Generates responses using OpenAI LLM with retrieved context
    """
    
    def __init__(self):
        """Initialize the response generator"""
        logger.info("Initializing response generator")
        settings = get_settings()
        openai.api_key = settings.openai_api_key
        self.model = settings.llm_model
    
    async def generate(self, query: str, documents: List[Dict[str, Any]], 
                      temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate response using LLM with document context
        
        Args:
            query: User query
            documents: Retrieved documents
            temperature: LLM temperature parameter
            
        Returns:
            Dict containing answer, sources, and confidence
        """
        try:
            logger.info(f"Generating response for query: {query[:50]}...")
            
            # Build context from documents
            context = self._build_context(documents)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            # Call LLM
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful EcoMarket assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            
            answer = response.choices[0].message.content
            
            # Extract sources
            sources = self._format_sources(documents)
            
            # Calculate confidence (simplified)
            confidence = self._calculate_confidence(documents)
            
            logger.info("Response generated successfully")
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from documents"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}: {doc['content']}")
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create prompt for LLM"""
        return f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
    
    def _format_sources(self, documents: List[Dict[str, Any]]) -> List[Dict]:
        """Format document sources for response"""
        return [
            {
                "content": doc['content'][:200],
                "metadata": doc.get('metadata', {})
            }
            for doc in documents
        ]
    
    def _calculate_confidence(self, documents: List[Dict[str, Any]]) -> float:
        """Calculate confidence score"""
        if not documents:
            return 0.0
        avg_distance = sum(doc.get('distance', 1.0) for doc in documents) / len(documents)
        return max(0.0, min(1.0, 1.0 - avg_distance))
