<script>
  import { Router, Route, Link } from 'svelte-routing';
  import Login from './components/Login.svelte';
  import Signup from './components/Signup.svelte';
  import MovieList from './components/MovieList.svelte';
  import CollabRecommendations from './components/CollabRecommendations.svelte';
</script>

<main>
  <!-- Wrap everything inside the Router component -->
  <Router>
    <!-- Navigation Links -->
    <nav>
      <Link to="/login">Login</Link> | 
      <Link to="/signup">Signup</Link> | 
      <Link to="/movies">Movies</Link> |
      <Link to="/collab-recommendations">Collab Recommendations</Link>
    </nav>

    <!-- Define routes inside the Router -->
    <Route path="/login" component="{Login}" />
    <Route path="/signup" component="{Signup}" />
    <Route path="/movies" component="{MovieList}" />
    <Route path="/collab-recommendations" component="{CollabRecommendations}" />
  </Router>
</main>

<style>
  nav {
    margin-bottom: 20px;
  }

  a {
    padding: 10px;
    text-decoration: none;
    color: #007BFF;
  }

  a:hover {
    color: #0056b3;
  }
</style>
