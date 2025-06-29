"""
Main product service that handles product-related queries
"""
import logging
from typing import Dict, Any, Optional

from services.rag_service import RAGService

logger = logging.getLogger(__name__)
from config import RAG_TOP_K
class ProductService:
    """Service for handling product-related queries"""
    
    def __init__(self):
        """Initialize the product service"""
        logger.info("Initializing Product service...")
        
        # Initialize RAG service to get chain
        rag_service = RAGService()
        self.rag_chain = rag_service.get_chain()
        
        logger.info("Product service initialized successfully")
    
    def handle_query(
        self, 
        messages: list[Dict[str,str]], 
        customer_id: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle a product-related query
        
        Args:
            query: The user's query
            customer_id: Optional customer ID
            metadata: Optional metadata
            
        Returns:
            Dict with response
        """

        query = " ".join([message["message"] for message in messages])
        
        lower_q = query.lower()
        
        # Simple intent check - redirect user to include customer ID for order-related queries
        
    
    # Add debug logging
        logger.info(f"Invoking RAG chain with query: {query}")
        logger.info(f"RAG_TOP_K value and type: {RAG_TOP_K} ({type(RAG_TOP_K)})")
    
        try:
        # Call the RAG chain
            response = self.rag_chain.invoke({"input": query})
            return response
        except Exception as e:
            logger.error(f"Error in RAG chain: {str(e)}")
            # Try to identify variables involved in the comparison
            # This is just a fallback response to avoid crashing
            return {
                "answer": "I'm sorry, I encountered an issue while processing your query. Our team has been notified.",
                "metadata": {"error": str(e)}
            }