import os
import sys

# Set project root (parent of 'scripts') in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from embeddings.cleaner import load_and_clean_data
from embeddings.splitter import split_documents
from embeddings.embedder import embed_and_store_in_pinecone
from init_pinecone import initialize_index

if __name__ == "__main__":
    initialize_index()
    raw_docs = load_and_clean_data("datasets/Product_Information_Dataset.csv")
    print("Raw docs created")
    processed_chunks = split_documents(raw_docs)
    print("Chunks processed")
    embed_and_store_in_pinecone(processed_chunks)
    print("✅ Data loading and embedding completed successfully.")
