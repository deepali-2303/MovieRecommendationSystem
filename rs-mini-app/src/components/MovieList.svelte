<script>
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  let movies = [];
  let selectedMovie = null;
  let recommendations = [];
  let movieInfo = null;
  let isLoading = false;

  onMount(async () => {
    isLoading = true;
    try {
      const response = await fetch("http://127.0.0.1:5000/top_movies");
      const topMovies = await response.json();
      movies = topMovies.map((movie) => movie.title);
    } catch (error) {
      console.error("Failed to fetch top movies:", error);
    } finally {
      isLoading = false;
    }
  });

  async function fetchRecommendations(movie) {
    isLoading = true;
    selectedMovie = movie;
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/recommend?title=${encodeURIComponent(movie)}`
      );
      recommendations = await response.json();
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
      recommendations = [];
    } finally {
      isLoading = false;
    }
  }

  async function fetchMovieInfo(movie) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/movie_info?title=${encodeURIComponent(movie)}`
      );
      movieInfo = await response.json();
    } catch (error) {
      console.error("Failed to fetch movie info:", error);
      movieInfo = null;
    }
  }

  function handleMovieSelect(movie) {
    fetchRecommendations(movie);
    fetchMovieInfo(movie);
  }

  function resetSelection() {
    selectedMovie = null;
    recommendations = [];
    movieInfo = null;
  }
</script>

<div class="container">
  {#if isLoading}
    <div class="loader" transition:fade></div>
  {:else if !selectedMovie}
    <div class="grid">
      {#each movies as movie}
        <button 
          class="movie-item" 
          on:click={() => handleMovieSelect(movie)}
        >
          {movie}
        </button>
      {/each}
    </div>
  {/if}

  {#if selectedMovie}
    <div class="details" transition:fade>
      <button class="back-btn" on:click={resetSelection}>← Back</button>
      
      {#if movieInfo}
        <div class="movie-info">
          <h1>{movieInfo.title}</h1>
          <div class="rating">★ {movieInfo.vote_average.toFixed(1)}</div>
          
          <p class="overview">{movieInfo.overview}</p>
          
          <div class="info-grid">
            <div>
              <h3>Details</h3>
              <p>Genre: {movieInfo.genres}</p>
              <p>Release: {movieInfo.release_date}</p>
              <p>Runtime: {movieInfo.runtime} mins</p>
              <p>Director: {movieInfo.director}</p>
            </div>
            
            <div>
              <h3>Cast</h3>
              <p>{movieInfo.cast}</p>
            </div>
          </div>
        </div>
      {/if}

      {#if recommendations.length > 0}
        <div class="recommendations">
          <h3>Recommended Movies</h3>
          <div class="recommendation-grid">
            {#each recommendations as recommendation}
              <button 
                class="recommendation-item" 
                on:click={() => handleMovieSelect(recommendation.title)}
              >
                {recommendation.title}
              </button>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  :root {
    --bg-primary: #121212;
    --text-primary: #f0f0f0;
    --accent: #3498db;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: var(--bg-primary);
    min-height: 100vh;
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  .movie-item {
    background-color: rgba(255,255,255,0.1);
    border: none;
    color: var(--text-primary);
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .movie-item:hover {
    background-color: rgba(255,255,255,0.2);
  }

  .details {
    text-align: left;
  }

  .back-btn {
    background: none;
    border: none;
    color: var(--accent);
    cursor: pointer;
    margin-bottom: 20px;
  }

  .movie-info h1 {
    color: var(--accent);
    margin-bottom: 10px;
  }

  .rating {
    color: gold;
    margin-bottom: 15px;
  }

  .overview {
    margin-bottom: 20px;
    line-height: 1.6;
  }

  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }

  .recommendations {
    margin-top: 30px;
  }

  .recommendation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }

  .recommendation-item {
    background-color: rgba(255,255,255,0.05);
    border: none;
    color: var(--text-primary);
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .recommendation-item:hover {
    background-color: rgba(255,255,255,0.1);
  }

  .loader {
    border: 3px solid rgba(255,255,255,0.3);
    border-top: 3px solid var(--accent);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 100px auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 600px) {
    .info-grid {
      grid-template-columns: 1fr;
    }
  }
</style>