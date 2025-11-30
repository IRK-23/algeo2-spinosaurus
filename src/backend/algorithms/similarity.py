import numpy as np
from typing import List, Tuple


def find_top_k_similar(query_idx: int, all_embeddings: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
    query_embedding = all_embeddings[query_idx]

    similarities = all_embeddings @ query_embedding

    similarities[query_idx] = -1.0

    top_k_indices = np.argsort(similarities)[::-1][:k]
    top_k_scores = similarities[top_k_indices]

    return [(int(idx), float(score)) for idx, score in zip(top_k_indices, top_k_scores)]
