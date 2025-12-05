import os
import json
from typing import List, Dict

from .pca_model import PCA


class PCAPreprocessing:
    def __init__(self, data_dir: str = "../../../data/", cache_dir: str = "./cache_pca", k: int = 100):
        self.data_dir = data_dir
        self.cache_dir = cache_dir
        self.k = k
        self.books = []
        self.pca_model = None

    def cache_exists(self) -> bool:
        required_files = [
            'u.npy',
            'uMatrix.npy',
            'coeffMatrix.npy',
            'books_metadata.json'
        ]
        return all(os.path.exists(os.path.join(self.cache_dir, f)) for f in required_files)

    def save_books_metadata(self):
        mapper_path = os.path.join(self.data_dir, 'mapper.json')
        with open(mapper_path, 'r', encoding='utf-8') as f:
            mapper = json.load(f)

        metadata = []
        for idx, (book_id, book_data) in enumerate(mapper.items()):
            metadata.append({
                'idx': idx,
                'id': book_id,
                'title': book_data['title'],
                'cover': book_data['cover']
            })

        with open(os.path.join(self.cache_dir, 'books_metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f)

    def load_books_metadata(self):
        with open(os.path.join(self.cache_dir, 'books_metadata.json'), 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        self.books = metadata
        return metadata

    def run_full_preprocessing(self):
        self.pca_model = PCA(k=self.k)
        self.pca_model.fit(self.data_dir)

        os.makedirs(self.cache_dir, exist_ok=True)
        self.pca_model.save(self.cache_dir)
        self.save_books_metadata()

    def load_from_cache(self):
        self.pca_model = PCA(k=self.k)
        self.pca_model.load(self.cache_dir)
        self.load_books_metadata()

    def initialize(self):
        if self.cache_exists():
            self.load_from_cache()
        else:
            self.run_full_preprocessing()

    def get_similar_books_by_uploaded_image(self, image_path: str, top_k: int = 5) -> List[Dict]:
        if not self.pca_model:
            return []

        indices, distances = self.pca_model.find_similar_to_uploaded(image_path, top_k)

        recommendations = []
        for i, idx in enumerate(indices):
            book = self.books[int(idx)]
            # Normalisasi jarak ke skor kemiripan (0-1)
            # Pakai toleransi kecil krn 1-(distances[i]/100000) bisa tdk tepat 1.0
            if distances[i] < 1e-5: similarity = 1.0
            else: similarity = max(0, 1-(distances[i]/100000))
            
            recommendations.append({
                'id': book['id'],
                'title': book['title'],
                'cover': book['cover'],
                'similarity': similarity
            })

        return recommendations
