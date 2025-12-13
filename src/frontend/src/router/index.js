import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ImageSearchView from '../views/ImageSearchView.vue'
import DocumentSearchView from '../views/DocumentSearchView.vue'
import BookDetailView from '../views/BookDetailView.vue'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home',
			component: HomeView
		},
		{
			path: '/search-image',
			name: 'image-search',
			component: ImageSearchView
		},
		{
			path: '/search-document',
			name: 'document-search',
			component: DocumentSearchView
		},
		{
			path: '/book/:id',
			name: 'book-detail',
			component: BookDetailView
		}
	]
})

export default router
