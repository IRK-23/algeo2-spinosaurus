import json
import os
from typing import List, Dict


def load_dataset(data_dir: str = "../../../data/") -> List[Dict[str, str]]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, data_dir)
    mapper_path = os.path.join(data_path, "mapper.json")

    with open(mapper_path, 'r', encoding='utf-8') as f:
        mapper = json.load(f)


    books = []

    for book_id, book_info in mapper.items():
        txt_path = os.path.join(data_path, book_info["txt"])

        if not os.path.exists(txt_path):
            print(f"File not found: {txt_path}")
            continue

        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()

            books.append({
                "id": book_id,
                "title": book_info["title"],
                "content": content,
                "cover": book_info["cover"]
            })


        except Exception as e:
            print(f"Error loading book {book_id}: {e}")
            continue

    return books

