from pinecone import Pinecone, ServerlessSpec
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME
def initialize_index(index_name=PINECONE_INDEX_NAME, dimension=1536):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"✅ Created Pinecone index '{index_name}'")
    else:
        print(f"ℹ️ Index '{index_name}' already exists")
