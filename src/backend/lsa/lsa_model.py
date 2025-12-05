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
        self.U_k = None
        self.sigma_k = None

    def fit(self, tfidf_matrix: csr_matrix):
        tfidf_dense = tfidf_matrix.toarray()

        U_k, sigma_k, V_k = truncated_svd(tfidf_dense, k=self.k)

        self.U_k = U_k
        self.sigma_k = sigma_k

        document_embeddings = V_k.T @ sigma_k

        self.document_embeddings_normalized = self.normalize_embeddings(document_embeddings)

        return self

    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        normalized = np.zeros_like(embeddings)
        for i in range(embeddings.shape[0]):
            length = vector_length(embeddings[i])
            if length > 1e-7:
                normalized[i] = embeddings[i] / length
            else:
                normalized[i] = embeddings[i]
        return normalized

    def get_similar_documents(self, doc_idx: int, top_k: int = 5) -> List[Tuple[int, float]]:

        return find_top_k_similar(doc_idx, self.document_embeddings_normalized, k=top_k)

    def find_query_embedding(self, query_tfidf_vector: np.ndarray) -> np.ndarray:
        if query_tfidf_vector.ndim == 1:
            query_tfidf_vector = query_tfidf_vector.reshape(-1, 1)

        sigma_k_inv = np.zeros_like(self.sigma_k)
        for i in range(self.k):
            if self.sigma_k[i, i] > 1e-7:
                sigma_k_inv[i, i] = 1.0 / self.sigma_k[i, i]

        query_embedding = (sigma_k_inv @ self.U_k.T @ query_tfidf_vector).T
        return query_embedding.flatten()

    def find_similar_to_query(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        query_length = vector_length(query_embedding)
        if query_length > 1e-7:
            query_normalized = query_embedding / query_length
        else:
            query_normalized = query_embedding

        similarities = self.document_embeddings_normalized @ query_normalized

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(int(idx), float(similarities[idx])) for idx in top_indices]

        return results

    def save(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        np.save(os.path.join(output_dir, 'document_embeddings_normalized.npy'), self.document_embeddings_normalized.astype(np.float32))
        np.save(os.path.join(output_dir, 'U_k.npy'), self.U_k.astype(np.float32))
        np.save(os.path.join(output_dir, 'sigma_k.npy'), self.sigma_k.astype(np.float32))

    def load(self, input_dir: str):
        self.document_embeddings_normalized = np.load(os.path.join(input_dir, 'document_embeddings_normalized.npy'))
        self.U_k = np.load(os.path.join(input_dir, 'U_k.npy'))
        self.sigma_k = np.load(os.path.join(input_dir, 'sigma_k.npy'))
        return self
