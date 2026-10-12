
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_index(chunks: list[str]):
    """Convert text chunks into embeddings and build a FAISS index."""

    if not chunks:
        raise ValueError("Cannot build an index with no text chunks.")

    # Load the pretrained embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Convert each chunk into a normalized vector
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # FAISS requires float32 vectors
    embeddings = np.asarray(embeddings, dtype=np.float32)

    # Exact similarity search using inner product
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return model, index


def retrieve(
    question: str,
    model,
    index,
    chunks: list[str],
    top_k: int = 8
):
    """Retrieve the most similar chunks for a question."""

    if not question.strip():
        return []

    k = min(top_k, len(chunks))

    # Embed the question using the same model
    query_vector = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype(np.float32)

    scores, indices = index.search(query_vector, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "chunk_id": int(idx),
            "text": chunks[int(idx)],
            "score": float(score)
        })

    return results
