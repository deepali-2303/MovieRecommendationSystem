<script>
  import { onMount } from "svelte";
  import { fade, scale } from "svelte/transition";
  import Recommendations from "./Recommendations.svelte";

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

  function handleMovieSelect(event, movie) {
    if (
      event.type === "click" ||
      (event.type === "keydown" && (event.key === "Enter" || event.key === " "))
    ) {
      fetchRecommendations(movie);
      fetchMovieInfo(movie);
    }
  }

  function resetSelection() {
    selectedMovie = null;
    recommendations = [];
    movieInfo = null;
  }
</script>

<div class="movie-app-container">
  <div class="glass-header">
    <h1>Movie Recommender</h1>
    {#if selectedMovie}
      <button 
        class="reset-btn" 
        on:click={resetSelection}
        transition:fade
      >
        ← Back to Movies
      </button>
    {/if}
  </div>

  {#if isLoading}
    <div class="loader-container" transition:fade>
      <div class="loader"></div>
    </div>
  {:else if !selectedMovie}
    <div class="movie-grid" transition:fade>
      {#each movies as movie}
        <button
          class="movie-card"
          on:click={(event) => handleMovieSelect(event, movie)}
          on:keydown={(event) => handleMovieSelect(event, movie)}
          transition:scale
        >
          <span>{movie}</span>
        </button>
      {/each}
    </div>
  {/if}

  {#if selectedMovie && recommendations.length > 0}
    <Recommendations {selectedMovie} {recommendations} />
  {/if}

  {#if movieInfo}
    <div class="movie-details-container" transition:fade>
      <div class="movie-details-card">
        <div class="movie-header">
          <h2>{movieInfo.title}</h2>
          <div class="movie-rating">
            <span>★</span>
            {movieInfo.vote_average.toFixed(1)}
          </div>
        </div>
        
        <div class="movie-info-grid">
          <div class="movie-info-section">
            <h3>Overview</h3>
            <p>{movieInfo.overview}</p>
          </div>
          
          <div class="movie-info-section">
            <h3>Details</h3>
            <ul>
              <li><strong>Genres:</strong> {movieInfo.genres}</li>
              <li><strong>Release Date:</strong> {movieInfo.release_date}</li>
              <li><strong>Runtime:</strong> {movieInfo.runtime} mins</li>
              <li><strong>Director:</strong> {movieInfo.director}</li>
            </ul>
          </div>
          
          <div class="movie-info-section cast">
            <h3>Cast</h3>
            <p>{movieInfo.cast}</p>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  :root {
    --bg-primary: #121212;
    --bg-secondary: #1e1e1e;
    --text-primary: #ffffff;
    --accent-color: #ff6b6b;
    --card-bg: rgba(30, 30, 30, 0.8);
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .movie-app-container {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #121212, #2a2a2a);
    min-height: 100vh;
    color: var(--text-primary);
    padding: 2rem;
  }

  .glass-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(30, 30, 30, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 12px;
  }

  .glass-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--accent-color);
  }

  .reset-btn {
    background: var(--accent-color);
    color: var(--text-primary);
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .reset-btn:hover {
    opacity: 0.9;
    transform: scale(1.05);
  }

  .movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    justify-content: center;
  }

  .movie-card {
    background: var(--card-bg);
    border: none;
    border-radius: 12px;
    padding: 1.5rem;
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
    text-align: center;
    font-weight: 600;
  }

  .movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    background: rgba(50, 50, 50, 0.9);
  }

  .movie-details-container {
    max-width: 900px;
    margin: 2rem auto;
  }

  .movie-details-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(10px);
  }

  .movie-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 1rem;
  }

  .movie-header h2 {
    font-size: 2.5rem;
    color: var(--accent-color);
  }

  .movie-rating {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    color: #ffd700;
  }

  .movie-rating span {
    margin-right: 0.5rem;
  }

  .movie-info-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
  }

  .movie-info-section {
    padding: 1rem 0;
  }

  .movie-info-section h3 {
    margin-bottom: 1rem;
    color: var(--accent-color);
  }

  .movie-info-section ul {
    list-style-type: none;
  }

  .movie-info-section li {
    margin-bottom: 0.5rem;
  }

  .cast {
    grid-column: span 2;
  }

  .loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  }

  .loader {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid var(--accent-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 768px) {
    .movie-info-grid {
      grid-template-columns: 1fr;
    }

    .movie-details-card {
      padding: 1rem;
    }

    .movie-header {
      flex-direction: column;
      text-align: center;
    }

    .movie-header h2 {
      margin-bottom: 1rem;
    }
  }
</style>