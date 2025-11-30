from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from lsa.preprocessing import Preprocessing
import json
import os

pipeline = None

def create_app():
    global pipeline
    app = Flask(__name__)
    CORS(app)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../data')

    pipeline = Preprocessing(data_dir="../../../data/", cache_dir="./cache", k=100)
    pipeline.initialize()

    @app.route('/')
    def hello():
        return "Hello from Flask Backend!"

    @app.route('/api/books', methods=['GET'])
    def get_books():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search_query = request.args.get('search', '').lower()

        filtered_books = pipeline.books
        if search_query:
            filtered_books = [b for b in pipeline.books if search_query in b['title'].lower()]

        total_books = len(filtered_books)
        start = (page - 1) * per_page
        end = start + per_page

        return jsonify({
            'books': filtered_books[start:end],
            'total': total_books,
            'page': page,
            'per_page': per_page
        })

    @app.route('/api/books/<book_id>', methods=['GET'])
    def get_book_detail(book_id):
        book = pipeline.get_book_by_id(book_id)
        if book:
            return jsonify(book)
        return jsonify({'error': 'Buku tidak ketemu'}), 404

    @app.route('/data/<path:filename>')
    def serve_data(filename):
        return send_from_directory(DATA_DIR, filename)

    # Sementara dulu, karena blm ada implementasi PCA dan LSA
    @app.route('/api/search/image', methods=['POST'])
    def search_by_image():
        # Placeholder sementara PCA image search
        # Seharusnya ini memproses gambar yg diupload
        # Utk sementara return buku random
        import random
        results = random.sample(pipeline.books, min(len(pipeline.books), 5)) if pipeline.books else []
        # Similarity score sementara/dummy
        for res in results:
            res['similarity'] = round(random.uniform(0.7, 0.99), 2)
        return jsonify({'results': results})

    @app.route('/api/books/<book_id>/recommendations', methods=['GET'])
    def get_recommendations(book_id):
        book = pipeline.get_book_by_id(book_id)
        if not book:
            return jsonify({'error': 'Buku tidak ketemu'}), 404

        book_idx = book['index']
        recommendations = pipeline.get_book_recommendations(book_idx, top_k=5)

        return jsonify({'recommendations': recommendations})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

