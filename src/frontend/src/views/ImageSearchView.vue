<template>
	<div class="image-search">
		<h1>Search by Image</h1>
		
		<div class="search-controls">
			<div class="upload-section" @dragover.prevent @drop.prevent="dropHandler">
				<label for="file-input" class="custom-file-upload">
					Upload Cover Image
				</label>
				<input type="file" id="file-input" @change="handleFileUpload" accept="image/*" />
				<span v-if="selectedFile">{{ selectedFile.name }}</span>
			</div>

			<div class="threshold-section">
				<label>Similarity Threshold: {{ threshold }}%</label>
				<input 
					type="range" 
					v-model="threshold" 
					min="0" 
					max="100" 
					step="1" 
				/>
			</div>

			<button @click="searchImage" :disabled="!selectedFile || loading" class="m3-btn">
				{{ loading ? 'Searching...' : 'Search' }}
			</button>
		</div>

		<div v-if="previewUrl" class="preview">
			<img :src="previewUrl" alt="Preview" />
		</div>

		<div v-if="results.length > 0" class="results">
			<h2>Hasil Pencarian</h2>
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
			Tidak ada buku yang ditemukan yang mirip.
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import BookCard from '../components/BookCard.vue';

const selectedFile = ref(null);
const previewUrl = ref(null);
const threshold = ref(70);
const results = ref([]);
const loading = ref(false);
const searched = ref(false);

const handleFileUpload = (event) => {
	const file = event.target.files[0];
	if (file) {
		selectedFile.value = file;
		previewUrl.value = URL.createObjectURL(file);
		results.value = [];
		searched.value = false;
	}
};

const dropHandler = (event) => {
	const file = event.dataTransfer.files[0];
	if (file && file.type.startsWith('image/')) {
		selectedFile.value = file;
		previewUrl.value = URL.createObjectURL(file);
		results.value = [];
		searched.value = false;
	}
};

const searchImage = async () => {
	if (!selectedFile.value) return;

	loading.value = true;
	searched.value = true;
	
	const formData = new FormData();
	formData.append('image', selectedFile.value);
	formData.append('threshold', threshold.value / 100);

	try {
		const response = await fetch('http://localhost:5000/api/search/image', {
			method: 'POST',
			body: formData
		});
		
		const data = await response.json();
		// Filter result berdasarkan threshold kalau backend tdk melakukannya
		results.value = data.results.filter(r => (r.similarity || 0) >= threshold.value / 100);
	} catch (error) {
		console.error('Error mencari gambar:', error);
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

.image-search {
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
	color: #f7f2fa;
	padding: 2rem;
	border-radius: 12px;
}

.upload-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
}

input[type="file"] {
	display: none;
}

.custom-file-upload {
	border: 2px dashed #f7f2fa;
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

.threshold-section {
	width: 100%;
	max-width: 400px;
}

input[type="range"] {
	width: 100%;
	margin-top: 0.5rem;
}

button {
	padding: 0.8rem 2rem;
	background-color: #42b983;
	color: white;
	border: none;
	border-radius: 8px;
	font-size: 1.1rem;
	cursor: pointer;
	transition: background-color 0.3s;
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

.m3-btn:hover {
	background-color: #B69DF8;
}

.m3-btn:disabled {
	background-color: #CCC2DC;
	cursor: not-allowed;
}

.preview {
	margin-bottom: 3rem;
}

.preview img {
	max-height: 300px;
	border-radius: 8px;
	box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.books-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 2rem;
	margin-top: 2rem;
}
</style>
