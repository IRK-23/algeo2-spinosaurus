<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
	<header>
		<div class="wrapper">
			<nav>
				<RouterLink to="/">Home</RouterLink>
				<RouterLink to="/search-image">Image Search</RouterLink>
			</nav>
		</div>
	</header>

	<RouterView />
</template>

<style scoped>
header {
	line-height: 1.5;
	background-color: #fff;
	box-shadow: 0 2px 8px rgba(0,0,0,0.1);
	padding: 1rem 0;
	margin-bottom: 2rem;
}

nav {
	width: 100%;
	font-size: 1.2rem;
	text-align: center;
}

nav a {
	display: inline-block;
	padding: 0 1rem;
	border-left: 1px solid #e0e0e0;
	text-decoration: none;
	color: #2c3e50;
	font-weight: 500;
	transition: color 0.3s;
}

nav a:first-of-type {
	border: 0;
}

nav a.router-link-active {
	color: #42b983;
}

nav a:hover {
	color: #3aa876;
}
</style>
