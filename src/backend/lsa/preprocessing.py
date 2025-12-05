import os
import json
from typing import List, Dict

from ..textPreprocessor.data_loader import load_dataset
from ..textPreprocessor.text_processor import preprocess_documents, TextPreprocessor
from ..textPreprocessor.document_indexer import build_matrix_from_documents
from ..textPreprocessor.tfidf import Tfidf
from .lsa_model import LSAModel
import numpy as np
from collections import Counter


class Preprocessing:
    def __init__(self, data_dir: str = "../../../data/", cache_dir: str = "./cache", k: int = 100):
        self.data_dir = data_dir
        self.cache_dir = cache_dir
        self.k = k
        self.books = []
        self.lsa_model = None
        self.vocabulary = None
        self.term_list = None
        self.tfidf_transformer = None

    def cache_exists(self) -> bool:
        required_files = [
            'document_embeddings_normalized.npy',
            'U_k.npy',
            'sigma_k.npy',
            'term_list.json',
            'idf_vector.npy',
            'books_metadata.json'
        ]
        return all(os.path.exists(os.path.join(self.cache_dir, f)) for f in required_files)

    def save_books_metadata(self):
        metadata = [
            {
                'id': book['id'],
                'title': book['title'],
                'cover': book['cover']
            }
            for book in self.books
        ]
        with open(os.path.join(self.cache_dir, 'books_metadata.json'), 'w') as f:
            json.dump(metadata, f)

    def load_books_metadata(self):
        with open(os.path.join(self.cache_dir, 'books_metadata.json'), 'r') as f:
            return json.load(f)

    def run_full_preprocessing(self):
        print("Loading docs...")
        self.books = load_dataset(self.data_dir)

        documents = [book['content'] for book in self.books]

        print("Preprocessing...")
        preprocessed_docs = preprocess_documents(documents)

        print("Building matrix...")
        term_doc_matrix, vocabulary, term_list = build_matrix_from_documents(preprocessed_docs)

        print("Computing TF-IDF...")
        tfidf_transformer = Tfidf()
        tfidf_matrix = tfidf_transformer.fit_transform(term_doc_matrix)

        self.vocabulary = vocabulary
        self.term_list = term_list
        self.tfidf_transformer = tfidf_transformer

        print("Applying LSA...")
        self.lsa_model = LSAModel(k=self.k)
        self.lsa_model.fit(tfidf_matrix)

        print("Caching...")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.lsa_model.save(self.cache_dir)
        self.save_books_metadata()

        with open(os.path.join(self.cache_dir, 'term_list.json'), 'w') as f:
            json.dump(term_list, f)
        np.save(os.path.join(self.cache_dir, 'idf_vector.npy'), tfidf_transformer.idf_vector.astype(np.float32))

    def load_from_cache(self):
        self.lsa_model = LSAModel(k=self.k)
        self.lsa_model.load(self.cache_dir)

        metadata = self.load_books_metadata()
        self.books = metadata

        with open(os.path.join(self.cache_dir, 'term_list.json'), 'r') as f:
            self.term_list = json.load(f)
        self.vocabulary = {term: idx for idx, term in enumerate(self.term_list)}

        idf_vector = np.load(os.path.join(self.cache_dir, 'idf_vector.npy'))
        self.tfidf_transformer = Tfidf()
        self.tfidf_transformer.idf_vector = idf_vector
        self.tfidf_transformer.num_terms = len(self.term_list)

    def initialize(self):
        if self.cache_exists():
            self.load_from_cache()
        else:
            self.run_full_preprocessing()

    def get_book_recommendations(self, book_idx: int, top_k: int = 5) -> List[Dict]:
        similar_docs = self.lsa_model.get_similar_documents(book_idx, top_k)

        recommendations = []
        for doc_idx, similarity in similar_docs:
            recommendations.append({
                'id': self.books[doc_idx]['id'],
                'title': self.books[doc_idx]['title'],
                'cover': self.books[doc_idx]['cover'],
                'similarity': similarity
            })

        return recommendations

    def get_book_by_id(self, book_id: str) -> Dict:
        for idx, book in enumerate(self.books):
            if book['id'] == book_id:
                return {'index': idx, **book}
        return None

    def search_by_document(self, document_text: str, top_k: int = 5) -> List[Dict]:
        preprocessor = TextPreprocessor()
        tokens = preprocessor.preprocess(document_text)

        term_freq = Counter(tokens)

        query_vector = np.zeros(len(self.term_list))
        for term, freq in term_freq.items():
            if term in self.vocabulary:
                term_idx = self.vocabulary[term]
                query_vector[term_idx] = freq

        query_tfidf = self.tfidf_transformer.transform_query(query_vector)

        query_embedding = self.lsa_model.find_query_embedding(query_tfidf)

        similar_docs = self.lsa_model.find_similar_to_query(query_embedding, top_k)

        recommendations = []
        for doc_idx, similarity in similar_docs:
            recommendations.append({
                'id': self.books[doc_idx]['id'],
                'title': self.books[doc_idx]['title'],
                'cover': self.books[doc_idx]['cover'],
                'similarity': similarity
            })

        return recommendations
