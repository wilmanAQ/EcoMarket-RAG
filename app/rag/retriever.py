"""
Document Retriever Module
Retrieves relevant documents using vector similarity search
"""

import chromadb
from typing import List, Dict, Any
from loguru import logger
from app.rag.embeddings import EmbeddingService


class DocumentRetriever:
    """
    Retrieves relevant documents using ChromaDB vector store
    """
    
    def __init__(self, embedding_service: EmbeddingService, 
                 collection_name: str = "ecomarket_docs"):
        """
        Initialize the document retriever
        
        Args:
            embedding_service: Service for generating embeddings
            collection_name: Name of the ChromaDB collection
        """
        logger.info(f"Initializing document retriever with collection: {collection_name}")
        self.embedding_service = embedding_service
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)
    
    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            logger.info(f"Retrieving documents for query: {query[:50]}...")
            
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            
            # Search in vector store
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            documents = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0.0
                    })
            
            logger.info(f"Retrieved {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
