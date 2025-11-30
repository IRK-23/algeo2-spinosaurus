[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/WQhgEYKW)
# Template Tugas Besar 2 Aljabar Linier dan Geometri

## Cara Menjalankan Program

1. Install [node.js, npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm), dan [Python](https://www.python.org/downloads/) kalau belum.
2. Clone repository ini.

    ```bash
    git clone https://github.com/IRK-23/algeo2-spinosaurus.git
    ```

3. Pindah ke folder backend, install requirements.txt, jalankan app.py

    ```bash
    cd src/backend
    pip install -r requirements.txt
    python app.py
    ```

4. Pindah ke folder frontend, install package dengan npm, jalankan frontend

    ```bash
    cd src/frontend

    # Kalau pakai nvm di Linux:
    source ~/.nvm/nvm.sh

    npm install
    npm run dev
    ```

## How to Develop
The template base file structure is as below
```
root
├───data
├───docs
├───src
│   ├───backend
│   └───frontend
├───test
├───.gitignore
├───README.md
└───LICENSE
```

### Purpose of each directory
1. `data`: to store application data, this should include huge datasets that is used in the applicaiton
2. `docs`: to store final report and other documents
3. `src`: to store source code of the application. Includes `frontend` and `backend` to store each respective component of the app
4. `test`: to store test cases