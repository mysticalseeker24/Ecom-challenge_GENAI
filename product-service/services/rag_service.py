"""
Service for RAG (Retrieval-Augmented Generation) functionality
"""
import logging
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from services.pinecone_service import PineconeService

logger = logging.getLogger(__name__)

class RAGService:
    """Service for RAG functionality"""
    
    def __init__(self):
        """Initialize the RAG service"""
        logger.info("Initializing RAG service...")
        
        # Initialize Pinecone service to get retriever
        pinecone_service = PineconeService()
        self.retriever = pinecone_service.get_retriever()
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=LLM_MODEL, 
            openai_api_key=OPENAI_API_KEY,
            temperature=LLM_TEMPERATURE
        )
        
        # Create prompt templates
        self._create_prompts()
        
        # Create RAG chain
        self._create_chain()
        
        logger.info("RAG service initialized successfully")
    
    def _create_prompts(self):
        """Create prompt templates for RAG"""
        # System Prompt
        system_template = SystemMessagePromptTemplate.from_template(
            """You are a helpful assistant that answers product-related questions using context provided.

            If the user asks about orders or delivery, always ask for their customer ID first before proceeding.
            If the user asks for a product recommendation, provide a brief summary of the product and its features. do not ask for customer ID.
            Always respond politely and ask follow-up questions if required to complete the user's request."""
        )

        # User prompt
        user_template = ChatPromptTemplate.from_template(
            "Context: {context}\n\nUser Question: {input}"
        )

        # Combine system + user
        self.prompt = system_template + user_template
    
    def _create_chain(self):
        """Create the RAG chain"""
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, document_chain)
    
    def get_chain(self):
        """Return the configured RAG chain"""
        return self.rag_chain