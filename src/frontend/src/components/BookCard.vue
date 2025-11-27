<template>
	<div class="book-card" @click="goToDetail">
		<div class="image-container">
			<img :src="imageUrl" :alt="book.title" loading="lazy" @error="handleImageError" />
		</div>
		<div class="info">
			<h3 :title="book.title">{{ book.title }}</h3>
			<p v-if="similarity !== null" class="similarity">Match: {{ (similarity * 100).toFixed(1) }}%</p>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
	book: {
		type: Object,
		required: true
	},
	similarity: {
		type: Number,
		default: null
	}
});

const router = useRouter();

const imageUrl = computed(() => {
	if (!props.book.cover) return 'https://via.placeholder.com/200x300?text=No+Cover';
	return `http://localhost:5000/data/${props.book.cover}`;
});

const handleImageError = (e) => {
	e.target.src = 'https://via.placeholder.com/200x300?text=Error';
};

const goToDetail = () => {
	router.push(`/book/${props.book.id}`);
};
</script>	

<style scoped>
.book-card {
	border: 1px solid #e0e0e0;
	border-radius: 12px;
	overflow: hidden;
	cursor: pointer;
	transition: all 0.3s ease;
	background: white;
	display: flex;
	flex-direction: column;
	height: 100%;
}

.book-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.image-container {
	aspect-ratio: 2/3;
	overflow: hidden;
	background: #f5f5f5;
	position: relative;
}

.image-container img {
	width: 100%;
	height: 100%;
	object-fit: cover;
	transition: transform 0.3s ease;
}

.book-card:hover .image-container img {
	transform: scale(1.05);
}

.info {
	padding: 1rem;
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

h3 {
	margin: 0;
	font-size: 1rem;
	font-weight: 600;
	line-height: 1.4;
	color: #2c3e50;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.similarity {
	margin-top: 0.5rem;
	font-size: 0.9rem;
	color: #27ae60;
	font-weight: 600;
}
</style>
