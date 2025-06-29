"""
Service for interacting with Pinecone vector database
"""
import logging
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from config import PINECONE_API_KEY, OPENAI_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL, RAG_TOP_K

logger = logging.getLogger(__name__)

class PineconeService:
    """Service for interacting with Pinecone vector database"""
    
    def __init__(self):
        """Initialize the Pinecone service"""
        logger.info("Initializing Pinecone service...")
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL, 
            openai_api_key=OPENAI_API_KEY
        )
        
        self.vectorstore = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            embedding=self.embeddings,
            pinecone_api_key=PINECONE_API_KEY
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )
        
        logger.info("Pinecone service initialized successfully")
    
    def get_retriever(self):
        """Return the configured retriever"""
        return self.retriever