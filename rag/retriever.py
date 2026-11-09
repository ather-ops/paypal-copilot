
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


RAG_DIR = Path(__file__).resolve().parent
VECTOR_STORE_DIR = RAG_DIR / "vector_store"

INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"
CHUNKS_PATH = VECTOR_STORE_DIR / "chunks.json"
CONFIG_PATH = VECTOR_STORE_DIR / "config.json"


class PayPalRetriever:

    def __init__(self):

        for path in [INDEX_PATH, CHUNKS_PATH, CONFIG_PATH]:
            if not path.exists():
                raise FileNotFoundError(f"Missing file: {path}")

        # Load chunks
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Load config
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # Load FAISS index
        self.index = faiss.read_index(str(INDEX_PATH))

        # Load embedding model
        self.embedding_model = SentenceTransformer(
            self.config["embed_model"]
        )

        # Validate vector store
        if self.index.ntotal != len(self.chunks):
            raise ValueError("FAISS index and chunks count mismatch")

        if self.index.d != self.config["dim"]:
            raise ValueError("Embedding dimension mismatch")

    def retrieve(
        self,
        query,
        top_k=5,
        document_type=None,
        dispute_type=None
    ):

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be positive")

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            self.index.ntotal
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            chunk = self.chunks[idx]
            metadata = chunk["metadata"]

            if (
                document_type
                and metadata.get("document_type") != document_type
            ):
                continue

            if (
                dispute_type
                and metadata.get("dispute_type") != dispute_type
            ):
                continue

            results.append({
                "text": chunk["text"],
                "metadata": metadata,
                "score": float(score)
            })

            if len(results) >= top_k:
                break

        return results


retriever = PayPalRetriever()
