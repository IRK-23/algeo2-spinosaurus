from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../data')
    MAPPER_PATH = os.path.join(DATA_DIR, 'mapper.json')
    
    try:
        with open(MAPPER_PATH, 'r') as f:
            books_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {MAPPER_PATH} not found. Starting with empty data.")
        books_data = {}
    
    # Convert dict to list for easier pagination/searching
    books_list = []
    for id, info in books_data.items():
        info['id'] = id
        books_list.append(info)

    @app.route('/')
    def hello():
        return "Hello from Flask Backend!"

    @app.route('/api/books', methods=['GET'])
    def get_books():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search_query = request.args.get('search', '').lower()
        
        filtered_books = books_list
        if search_query:
            filtered_books = [b for b in books_list if search_query in b['title'].lower()]
            
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
        book = books_data.get(book_id)
        if book:
            response_data = book.copy()
            response_data['id'] = book_id
            return jsonify(response_data)
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
        results = random.sample(books_list, min(len(books_list), 5)) if books_list else []
        # Similarity score sementara/dummy
        for res in results:
            res['similarity'] = round(random.uniform(0.7, 0.99), 2)
        return jsonify({
            'results': results
        })

    @app.route('/api/books/<book_id>/recommendations', methods=['GET'])
    def get_recommendations(book_id):
        # Placeholder sementara rekomendasi LSA
        import random
        recommendations = random.sample(books_list, min(len(books_list), 5)) if books_list else []
        return jsonify({
            'recommendations': recommendations
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
