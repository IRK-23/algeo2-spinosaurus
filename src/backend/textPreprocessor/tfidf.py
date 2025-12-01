import numpy as np
from scipy.sparse import csr_matrix
from typing import Tuple


class Tfidf:
    def __init__(self):
        self.idf_vector = None
        self.num_documents = 0
        self.num_terms = 0

    def fit(self, term_doc_matrix: csr_matrix):
        self.num_terms, self.num_documents = term_doc_matrix.shape

        # df_i = jumlah dokumen dengan term i
        df = np.array((term_doc_matrix > 0).sum(axis=1)).flatten()

        # IDF[i] = log10(n / (1 + df_i))
        self.idf_vector = np.log10(self.num_documents / (1 + df))

        return self

    def transform(self, term_doc_matrix: csr_matrix) -> csr_matrix:

        doc_lengths = np.array(term_doc_matrix.sum(axis=0)).flatten()
        doc_lengths[doc_lengths == 0] = 1
        tf_matrix = term_doc_matrix.multiply(1.0 / doc_lengths).tocsr()

        # TF-IDF = diag(IDF) * TF
        # Manual multiplication
        tfidf_matrix = tf_matrix.copy()
        for i in range(self.num_terms):
            tfidf_matrix.data[tfidf_matrix.indptr[i]:tfidf_matrix.indptr[i+1]] *= self.idf_vector[i]

        return tfidf_matrix

    def fit_transform(self, term_doc_matrix: csr_matrix) -> csr_matrix:
        return self.fit(term_doc_matrix).transform(term_doc_matrix)


def compute_tfidf(term_doc_matrix: csr_matrix) -> Tuple[csr_matrix, np.ndarray]:
    tfidf = Tfidf()
    tfidf_matrix = tfidf.fit_transform(term_doc_matrix)
    return tfidf_matrix, tfidf.idf_vector



