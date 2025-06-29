from langchain_openai import OpenAIEmbeddings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, config):
        self.config = config
        self.embeddings = self._initialize_embeddings()
        logger.info("Embedding model initialized")

    def _initialize_embeddings(self):
        """
        Initialize the embedding model
        """
        return OpenAIEmbeddings(
            model="text-embedding-ada-002", 
            openai_api_key=self.config.OPENAI_API_KEY
        )
    
    def get_embeddings(self):
        """
        Return the initialized embedding model
        """
        return self.embeddings
    
    def embed_query(self, query):
        """
        Embed a single query string
        """
        return self.embeddings.embed_query(query)
    
    def embed_documents(self, documents):
        """
        Embed a list of documents
        """
        return self.embeddings.embed_documents(documents)