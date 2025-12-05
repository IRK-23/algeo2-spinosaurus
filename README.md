# Spinosaurus

## Penjelasan Singkat Program

Spinosaurus adalah aplikasi E-Library yang memanfaatkan konsep aljabar linear. Aplikasi ini memungkinkan pengguna untuk mencari buku berdasarkan teks judul, kemiripan visual sampul buku (menggunakan Principal Component Analysis), dan kemiripan semantik konten teks (menggunakan Latent Semantic Analysis). Aplikasi ini dibangun dengan Vue.js di sisi frontend dan Flask di sisi backend. Aplikasi ini mendemonstrasikan penerapan algoritma SVD (Singular Value Decomposition) dan eigenvalue dalam kasus information retrieval.

## Alur Program

1. Inisialisasi dan preprocessing:
    * Saat server dinyalakan, sistem menge-load dataset buku (gambar sampul dan teks konten).
    * PCA: Mengubah gambar jadi grayscale, mereduksi dimensi menggunakan SVD untuk mendapatkan eigenfaces, dan memproyeksikan seluruh gambar sampul buku ke ruang vektor fitur.
    * Modul LSA: Melakukan *text preprocessing* (tokenisasi, *stopword removal*, *stemming*), membangun matriks *Term-Document*, menerapkan pembobotan TF-IDF, dan mereduksi dimensi menggunakan SVD untuk menangkap hubungan semantik antar dokumen.
    * Hasil pemrosesan disimpan (*caching*) untuk efisiensi.

2. Pencarian gambar:
    * Pengguna meng-upload gambar sampul.
    * Gambar diproses dan diproyeksikan ke ruang eigenfaces yang telah dibentuk.
    * Program menghitung jarak Euclidean antara vektor gambar query dengan vektor gambar di database.
    * Program mengembalikan buku dengan jarak terdekat (tingkat kemiripan tertinggi).

3.  Pencarian dokumen:
    * Pengguna mengunggah file teks (`.txt`).
    * Teks diproses menjadi vektor TF-IDF dan diproyeksikan ke ruang LSA.
    * Program menghitung Cosine Similarity antara vektor query dengan vektor dokumen di database.
    * Program mengembalikan buku dengan konten yang paling relevan secara semantik.

4.  Rekomendasi buku:
    * Saat pengguna melihat detail buku, sistem secara otomatis mencari buku lain yang memiliki vektor LSA terdekat dengan buku yang sedang dilihat, sebagai rekomendasi buku lainnya.

## Cara Menjalankan Program

1. Install [node.js, npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), dan [Python](https://www.python.org/downloads/) kalau belum.
2. Clone repository ini.

    ```bash
    git clone https://github.com/IRK-23/algeo2-spinosaurus.git
    ```

3. Pindah ke folder backend, install requirements.txt, kembali ke algeo2-spinosaurus, jalankan app.py

    ```bash
    cd src/backend
    pip install -r requirements.txt
    cd ..
    cd ..
    python -m src.backend.app
    ```

4. Pindah ke folder frontend, install package dengan npm, jalankan frontend

    ```bash
    cd src/frontend

    # Kalau pakai nvm di Linux (bash):
    source ~/.nvm/nvm.sh

    npm install
    npm run dev
    ```