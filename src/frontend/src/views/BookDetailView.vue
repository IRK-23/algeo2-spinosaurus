<template>
	<div class="book-detail" v-if="book">
		<div class="detail-container">
			<div class="cover-section">
				<img :src="imageUrl" :alt="book.title" />
			</div>
			<div class="info-section">
				<h1>{{ book.title }}</h1>
				<div class="content-preview">
					<h3>Content Preview</h3>
					<pre class="book-text">{{ bookContent || 'Loading content...' }}</pre>
				</div>
			</div>
		</div>

		<div class="recommendations">
			<h2>Related Books</h2>
			<div v-if="loadingRecs" class="loading">Loading recommendations...</div>
			<div v-else class="books-grid">
				<BookCard 
					v-for="rec in recommendations" 
					:key="rec.id" 
					:book="rec" 
				/>
			</div>
		</div>
	</div>
	<div v-else-if="loading" class="loading">Loading book details...</div>
	<div v-else class="error">Book not found</div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import BookCard from '../components/BookCard.vue';

const route = useRoute();
const book = ref(null);
const bookContent = ref('');
const recommendations = ref([]);
const loading = ref(true);
const loadingRecs = ref(false);

const imageUrl = computed(() => {
	if (!book.value || !book.value.cover) return 'https://via.placeholder.com/300x450?text=No+Cover';
	return `http://localhost:5000/data/${book.value.cover}`;
});

const fetchBook = async (id) => {
	loading.value = true;
    bookContent.value = '';
	try {
		const response = await fetch(`http://localhost:5000/api/books/${id}`);
		if (response.ok) {
			book.value = await response.json();
            
            if (book.value.txt) {
                fetch(`http://localhost:5000/data/${book.value.txt}`)
                    .then(res => res.text())
                    .then(text => bookContent.value = text)
                    .catch(err => console.error('Error loading text:', err));
            }

			fetchRecommendations(id);
		}
	} catch (error) {
		console.error('Error fetching book:', error);
	} finally {
		loading.value = false;
	}
};

const fetchRecommendations = async (id) => {
	loadingRecs.value = true;
	try {
		const response = await fetch(`http://localhost:5000/api/books/${id}/recommendations`);
		const data = await response.json();
		recommendations.value = data.recommendations;
	} catch (error) {
		console.error('Error fetching recommendations:', error);
	} finally {
		loadingRecs.value = false;
	}
};

onMounted(() => {
	fetchBook(route.params.id);
});

// Watch for route changes to reload data when navigating between books
watch(() => route.params.id, (newId) => {
	if (newId) {
		fetchBook(newId);
		window.scrollTo(0, 0);
	}
});
</script>

<style scoped>
.book-detail {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem;
}

.detail-container {
	display: flex;
	gap: 3rem;
	margin-bottom: 4rem;
	align-items: flex-start;
}

.cover-section {
	flex: 0 0 300px;
}

.cover-section img {
	width: 100%;
	border-radius: 12px;
	box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.info-section {
	flex: 1;
}

h1 {
	font-size: 2.5rem;
	margin-bottom: 2rem;
	color: #2c3e50;
}

.content-preview {
	background: #f9f9f9;
	padding: 2rem;
	border-radius: 12px;
}

.book-text {
    white-space: pre-wrap;
    font-family: monospace;
    max-height: 500px;
    overflow-y: auto;
    background: #fff;
    padding: 1rem;
    border: 1px solid #eee;
    border-radius: 4px;
}

.recommendations h2 {
	font-size: 2rem;
	margin-bottom: 2rem;
	color: #2c3e50;
	border-bottom: 2px solid #eee;
	padding-bottom: 1rem;
}

.books-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 2rem;
}

@media (max-width: 768px) {
	.detail-container {
		flex-direction: column;
		align-items: center;
	}
	
	.cover-section {
		width: 200px;
		flex: 0 0 auto;
	}
}
</style>
