import os
import json
from typing import List, Dict

from ..textPreprocessor.data_loader import load_dataset
from ..textPreprocessor.text_processor import preprocess_documents
from ..textPreprocessor.document_indexer import build_matrix_from_documents
from ..textPreprocessor.tfidf import compute_tfidf
from .lsa_model import LSAModel


class Preprocessing:
    def __init__(self, data_dir: str = "../../../data/", cache_dir: str = "./cache", k: int = 100):
        self.data_dir = data_dir
        self.cache_dir = cache_dir
        self.k = k
        self.books = []
        self.lsa_model = None

    def cache_exists(self) -> bool:
        required_files = [
            'document_embeddings_normalized.npy',
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
        tfidf_matrix, idf_vector = compute_tfidf(term_doc_matrix)

        print("Applying LSA...")
        self.lsa_model = LSAModel(k=self.k)
        self.lsa_model.fit(tfidf_matrix)

        print("Caching...")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.lsa_model.save(self.cache_dir)
        self.save_books_metadata()

    def load_from_cache(self):
        self.lsa_model = LSAModel(k=self.k)
        self.lsa_model.load(self.cache_dir)

        metadata = self.load_books_metadata()
        self.books = metadata

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
