from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME


def embed_and_store_in_pinecone(text_chunks: list[str], index_name: str = PINECONE_INDEX_NAME):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY
    )
    vectorstore.add_texts(text_chunks)
    print(f"✅ Successfully stored {len(text_chunks)} chunks into Pinecone.")
