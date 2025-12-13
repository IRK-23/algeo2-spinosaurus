<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeIcon from '@/assets/home.svg'
import ImageSearchIcon from '@/assets/image_search.svg'
import DocumentSearchIcon from '@/assets/document_search.svg'
</script>

<template>
	<header>
		<div class="wrapper">
			<nav>
				<RouterLink to="/">
					<div class="icon-container">
						<img :src="HomeIcon" alt="Home" class="nav-icon" />
					</div>
					<span>Home</span>
				</RouterLink>
				<RouterLink to="/search-image">
					<div class="icon-container">
						<img :src="ImageSearchIcon" alt="Image Search" class="nav-icon" />
					</div>
					<span>Image Search</span>
				</RouterLink>
				<RouterLink to="/search-document">
					<div class="icon-container">
						<img :src="DocumentSearchIcon" alt="Document Search" class="nav-icon" />
					</div>
					<span>Document Search</span>
				</RouterLink>
			</nav>
		</div>
	</header>

	<RouterView />
</template>

<style scoped>
header {
	line-height: 1.5;
	background-color: #211f21;
	box-shadow: 0 2px 8px rgba(0,0,0,0.1);
	padding: 5px 0;
	margin-bottom: 2rem;
}

nav {
	width: 100%;
	font-size: 1rem;
	text-align: center;
	display: flex;
	justify-content: center;
	gap: 2rem;
}

nav a {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 0.5rem 1rem;
	text-decoration: none;
	color: #CCC2DC;
	font-weight: 500;
	transition: color 0.3s, background-color 0.3s;
	border-radius: 8px;
}

nav a.router-link-active {
	color: #CCC2DC;
}

nav a:hover {
	color: #CCC2DC;
}

.nav-icon {
	width: 24px;
	height: 24px;
}

.icon-container {
	padding: 4px 20px;
	border-radius: 16px;
	margin-bottom: 0.25rem;
	transition: background-color 0.3s;
	display: flex;
	align-items: center;
	justify-content: center;
}

/* Pill background */
nav a.router-link-active .icon-container {
	background-color: #45455a;
	border-radius: 9999px;
}
nav a.router-link-active:hover .icon-container {
	background-color: #504F63;
}
nav a:hover .icon-container {
	background-color: #2E2C2E;
}

/* nav a.router-link-active .nav-icon,
nav a:hover .nav-icon {
	
} */
</style>
