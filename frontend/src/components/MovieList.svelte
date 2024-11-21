<script>
  import { onMount } from "svelte";
  import Recommendations from "./Recommendations.svelte";

  let movies = [];
  let selectedMovie = null;
  let recommendations = [];
  let movieInfo = null;

  onMount(async () => {
    const response = await fetch("http://127.0.0.1:5000/top_movies");
    const topMovies = await response.json();
    movies = topMovies.map((movie) => movie.title);
  });

  async function fetchRecommendations(movie) {
    selectedMovie = movie;
    const response = await fetch(
      `http://127.0.0.1:5000/recommend?title=${encodeURIComponent(movie)}`
    );
    recommendations = await response.json();
  }

  async function fetchMovieInfo(movie) {
    const response = await fetch(
      `http://127.0.0.1:5000/movie_info?title=${encodeURIComponent(movie)}`
    );
    movieInfo = await response.json();
  }

  function handleMovieSelect(event, movie) {
    if (
      event.type === "click" ||
      (event.type === "keydown" && (event.key === "Enter" || event.key === " "))
    ) {
      fetchRecommendations(movie);
      fetchMovieInfo(movie);
    }
  }
</script>

<div class="bg-gradient-to-b from-black via-gray-900 to-gray-800 min-h-screen text-white">
  <div class="text-red-500">
    If this text is red, Tailwind is working!
  </div>
  
  <div class="container mx-auto py-8 px-4">
    <h2 class="text-3xl font-bold mb-6 text-center text-red-500">Top 10 Movies</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each movies as movie}
        <button
          class="movie-item p-4 bg-gray-800 hover:bg-gray-700 rounded-lg shadow-md transition-transform transform hover:-translate-y-2 focus:outline-none focus:ring-4 focus:ring-red-500"
          on:click={(event) => handleMovieSelect(event, movie)}
          on:keydown={(event) => handleMovieSelect(event, movie)}
        >
          {movie}
        </button>
      {/each}
    </div>

    {#if selectedMovie && recommendations.length > 0}
      <Recommendations {selectedMovie} {recommendations} />
    {/if}

    {#if movieInfo}
      <div class="movie-info mt-8 bg-gray-900 p-6 rounded-lg shadow-md">
        <h3 class="text-2xl font-semibold mb-4">{movieInfo.title}</h3>
        <p class="mb-2"><span class="font-bold text-red-500">Genres:</span> {movieInfo.genres}</p>
        <p class="mb-2"><span class="font-bold text-red-500">Release Date:</span> {movieInfo.release_date}</p>
        <p class="mb-2"><span class="font-bold text-red-500">Overview:</span> {movieInfo.overview}</p>
        <p class="mb-2"><span class="font-bold text-red-500">Runtime:</span> {movieInfo.runtime} mins</p>
        <p class="mb-2"><span class="font-bold text-red-500">Director:</span> {movieInfo.director}</p>
        <p class="mb-2"><span class="font-bold text-red-500">Cast:</span> {movieInfo.cast}</p>
        <p><span class="font-bold text-red-500">Rating:</span> {movieInfo.vote_average}</p>
      </div>
    {/if}
  </div>
</div>

<style>
  /* Custom styles for focus states */
  .movie-item:focus {
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.5);
  }
</style>
