<template>
	<div class="home">
		<div class="hero">
			<h1>Spinosaurus E-Library</h1>
			<div class="search-bar">
				<input 
					v-model="searchQuery" 
					@keyup.enter="handleSearch" 
					type="text" 
					placeholder="Search books by title..."
					class="m3-search-bar"
				/>
				<button @click="handleSearch" class="m3-btn">Search</button>
			</div>
		</div>

		<div v-if="loading" class="loading">Loading books...</div>
		
		<div v-else class="content">
			<div v-if="books.length === 0" class="no-results">
				No books found.
			</div>
			
			<div class="books-grid">
				<BookCard 
					v-for="book in books" 
					:key="book.id" 
					:book="book" 
				/>
			</div>

			<div class="pagination" v-if="totalPages > 1">
				<button 
					:disabled="currentPage === 1" 
					@click="changePage(currentPage - 1)"
					class="m3-btn"
				>
					Previous
				</button>
				<span>Page {{ currentPage }} of {{ totalPages }}</span>
				<button 
					:disabled="currentPage === totalPages" 
					@click="changePage(currentPage + 1)"
					class="m3-btn"
				>
					Next
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BookCard from '../components/BookCard.vue';

const books = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const currentPage = ref(1);
const totalPages = ref(1);
const perPage = 20;

const fetchBooks = async () => {
	loading.value = true;
	try {
		const query = new URLSearchParams({
			page: currentPage.value,
			per_page: perPage,
			search: searchQuery.value
		}).toString();
		
		const response = await fetch(`http://localhost:5000/api/books?${query}`);
		const data = await response.json();
		
		books.value = data.books;
		totalPages.value = Math.ceil(data.total / perPage);
	} catch (error) {
		console.error('Error fetching books:', error);
	} finally {
		loading.value = false;
	}
};

const handleSearch = () => {
	currentPage.value = 1;
	fetchBooks();
};

const changePage = (page) => {
	if (page >= 1 && page <= totalPages.value) {
		currentPage.value = page;
		fetchBooks();
		window.scrollTo(0, 0);
	}
};

onMounted(() => {
	fetchBooks();
});
</script>

<style scoped>
.home {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem;
}

.hero {
	text-align: center;
	margin-bottom: 3rem;
}

h1 {
	font-size: 2.5rem;
	color: #F7F2FA;
	margin-bottom: 1.5rem;
}

.search-bar {
	display: flex;
	justify-content: center;
	gap: 1rem;
	max-width: 600px;
	margin: 0 auto;
}

input {
	flex-grow: 1;
	padding: 0.8rem 1.2rem;
	border: 2px solid #e0e0e0;
	border-radius: 8px;
	font-size: 1rem;
	transition: border-color 0.3s;
}
.m3-search-bar {
	background-color: #2B2930;
	color: #CAC4D0;
	border-radius: 9999px;
	border: none;
}

input:focus {
	outline: none;
	border-color: #42b983;
}

button {
	padding: 0.8rem 1.5rem;
	background-color: #42b983;
	color: white;
	border: none;
	border-radius: 8px;
	font-size: 1rem;
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

button:hover {
	background-color: #B69DF8;
}

button:disabled {
	background-color: #CCC2DC;
	color: #332D41;
	cursor: not-allowed;
}

span {
	color: #F7F2FA;
}

.books-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 2rem;
	margin-bottom: 3rem;
}

.pagination {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1.5rem;
	margin-top: 2rem;
}

.loading, .no-results {
	text-align: center;
	font-size: 1.2rem;
	color: #666;
	margin-top: 3rem;
}
</style>
