import numpy as np
from scipy.sparse import csr_matrix
from typing import List, Dict, Tuple
from collections import Counter


class DocumentIndexer:
    def __init__(self):
        self.vocabulary = {}  # term -> index mapping
        self.term_list = []   # index -> term mapping
        self.term_doc_matrix = None
        self.num_documents = 0
        self.num_terms = 0

    def build_vocabulary(self, preprocessed_documents: List[List[str]]) -> Dict[str, int]:

        all_terms = set()
        for doc_tokens in preprocessed_documents:
            all_terms.update(doc_tokens)

        sorted_terms = sorted(all_terms)

        self.vocabulary = {term: idx for idx, term in enumerate(sorted_terms)}
        self.term_list = sorted_terms
        self.num_terms = len(self.vocabulary)

        return self.vocabulary

    def build_term_document_matrix(self, preprocessed_documents: List[List[str]]) -> csr_matrix:
        self.num_documents = len(preprocessed_documents)

        if not self.vocabulary:
            self.build_vocabulary(preprocessed_documents)


        rows = []  # term
        cols = []  # doc
        data = []  # freq

        for doc_idx, doc_tokens in enumerate(preprocessed_documents):
            term_freq = Counter(doc_tokens)

            for term, freq in term_freq.items():
                if term in self.vocabulary:
                    term_idx = self.vocabulary[term]
                    rows.append(term_idx)
                    cols.append(doc_idx)
                    data.append(freq)

            

        self.term_doc_matrix = csr_matrix(
            (data, (rows, cols)),
            shape=(self.num_terms, self.num_documents),
            dtype=np.float64
        )


        return self.term_doc_matrix



def build_matrix_from_documents(preprocessed_documents: List[List[str]]) -> Tuple[csr_matrix, Dict[str, int], List[str]]:
    indexer = DocumentIndexer()
    matrix = indexer.build_term_document_matrix(preprocessed_documents)
    return matrix, indexer.vocabulary, indexer.term_list



