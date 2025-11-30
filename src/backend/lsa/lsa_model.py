import numpy as np
from scipy.sparse import csr_matrix
from typing import Tuple, List
import os

from ..algorithms.svd import truncated_svd
from ..algorithms.similarity import find_top_k_similar
from ..algorithms.eigenvalue import vector_length


class LSAModel:
    def __init__(self, k: int = 100):
        self.k = k
        self.document_embeddings_normalized = None

    def fit(self, tfidf_matrix: csr_matrix):
        tfidf_dense = tfidf_matrix.toarray()

        U_k, sigma_k, V_k = truncated_svd(tfidf_dense, k=self.k)

        document_embeddings = V_k.T @ sigma_k

        self.document_embeddings_normalized = self.normalize_embeddings(document_embeddings)

        return self

    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        normalized = np.zeros_like(embeddings)
        for i in range(embeddings.shape[0]):
            length = vector_length(embeddings[i])
            if length > 1e-10:
                normalized[i] = embeddings[i] / length
            else:
                normalized[i] = embeddings[i]
        return normalized

    def get_similar_documents(self, doc_idx: int, top_k: int = 5) -> List[Tuple[int, float]]:

        return find_top_k_similar(doc_idx, self.document_embeddings_normalized, k=top_k)

    def save(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        np.save(os.path.join(output_dir, 'document_embeddings_normalized.npy'), self.document_embeddings_normalized)

    def load(self, input_dir: str):
        self.document_embeddings_normalized = np.load(os.path.join(input_dir, 'document_embeddings_normalized.npy'))
        return self
