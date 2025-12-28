import chromadb
from chromadb.utils import embedding_functions

def get_client():
    return chromadb.PersistentClient(path="data/chroma")

def get_collection():
    client = get_client()
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return client.get_or_create_collection(name="docs", embedding_function=ef)
