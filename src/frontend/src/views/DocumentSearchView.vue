<template>
	<div class="document-search">
		<h1>Search by Document</h1>
		
		<div class="search-controls">
			<div class="upload-section" @dragover.prevent @drop.prevent="dropHandler">
				<label for="file-input" class="custom-file-upload">
					Upload Text Document (.txt)
				</label>
				<input type="file" id="file-input" @change="handleFileUpload" accept=".txt" />
                <span class="file-name" v-if="selectedFile">{{ selectedFile.name }}</span>
			</div>

			<div class="top-k-section">
				<label>Top K Results: </label>
				<input
                    class="top-k-input"
					type="number" 
					v-model="topK" 
				/>
			</div>

			<button @click="searchDocument" :disabled="!selectedFile || loading" class="m3-btn">
				{{ loading ? 'Searching...' : 'Search' }}
			</button>
		</div>

        <div v-if="fileContent" class="preview-text">
            <h3>File Content Preview:</h3>
            <p>{{ fileContent }}</p>
        </div>

		<div v-if="results.length > 0" class="results">
			<h2>Search Results</h2>
			<div class="books-grid">
				<BookCard 
					v-for="book in results" 
					:key="book.id" 
					:book="book" 
					:similarity="book.similarity"
				/>
			</div>
		</div>
		
		<div v-else-if="searched && results.length === 0" class="no-results">
			No similar documents found.
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import BookCard from '../components/BookCard.vue';

const selectedFile = ref(null);
const fileContent = ref("");
const topK = ref(5);
const results = ref([]);
const loading = ref(false);
const searched = ref(false);

const handleFileUpload = (event) => {
	const file = event.target.files[0];
	processFile(file);
};

const dropHandler = (event) => {
	const file = event.dataTransfer.files[0];
	processFile(file);
};

const processFile = (file) => {
    if (file && file.type === 'text/plain') {
		selectedFile.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            fileContent.value = e.target.result;
        };
        reader.readAsText(file);
		results.value = [];
		searched.value = false;
	} else {
        alert("Please upload a valid .txt file");
    }
}

const searchDocument = async () => {
	if (!selectedFile.value) return;

	loading.value = true;
	searched.value = true;
	
	const formData = new FormData();
	formData.append('file', selectedFile.value);
	formData.append('top_k', topK.value);

	try {
		const response = await fetch('http://localhost:5000/api/search/document', {
			method: 'POST',
			body: formData
		});
		
		const data = await response.json();
		results.value = data.results;
	} catch (error) {
		console.error('Error mencari buku:', error);
	} finally {
		loading.value = false;
	}
};
</script>

<style scoped>
h1, h2 {
	color: #f7f2fa;
}

.no-results {
	color: #f7f2fa;
	font-size: 1.5rem;
}

.document-search {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem;
    text-align: center;
}

.search-controls {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	margin-bottom: 3rem;
	background: #211F26;
    color: #E6E0E9;
	padding: 2rem;
	border-radius: 12px;
}

.upload-section {
	/* padding: 2rem;
	border-radius: 8px;
	text-align: center;
	width: 100%;
	max-width: 500px;
	cursor: pointer;
	transition: border-color 0.3s; */
    display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
}

/* .upload-section:hover {
	border-color: #d0bcff;
} */

input[type="file"] {
	display: none;
}

.custom-file-upload {
    border: 2px dashed #E6E0E9;
	display: inline-block;
	padding: 1rem 2rem;
	cursor: pointer;
	font-weight: 500;
    border-radius: 8px;
	transition: all 0.3s;
}
.custom-file-upload:hover {
	border-color: #d0bcff;
	color: #d0bcff;
}

.top-k-input {
    width: 60px;
    padding: 6px 8px;
    border: 2px solid #666;
    border-radius: 8px;
    text-align: center;
    background: #1d1b20;
    color: #f7f2fa;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type=number] {
    appearance: textfield;
    -moz-appearance: textfield;
}

.top-k-section {
	color: #f7f2fa;
    display: flex;
	align-items: center;
	gap: 1rem;
}

.m3-btn {
	padding: 0.5rem 1rem;
	background-color: #D0BCFF;
	color: #381E72;
	border: none;
	border-radius: 9999px;
	font-size: 18px;
	font-weight: 500;
	cursor: pointer;
}

.m3-btn:disabled {
	background-color: #49454f;
	color: #1d1b20;
	cursor: not-allowed;
}

.preview-text {
    background: #1d1b20;
    color: #f7f2fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
    text-align: left;
    padding-top: 0;
    padding-bottom: 0;
}

.books-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 2rem;
}
</style>
