import faiss
from sentence_transformers import SentenceTransformer
import smolagents
print("Imports successful!")

print("Downloading/loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully!")
