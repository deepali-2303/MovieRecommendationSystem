<script>
  import { onMount } from 'svelte';
  import * as jwt_decode from 'jwt-decode';


  // Sample userId (You will dynamically fetch or pass this from your app)
  let userId = 1; // Replace this with the actual user ID when available
  let recommendedMovies = [];
  let errorMessage = '';

  // Fetch the collaborative recommendations from the API based on userId
  async function fetchRecommendations() {
  const token = localStorage.getItem('jwt_token'); // Retrieve token from localStorage
  
  if (!token) {
    throw new Error('No token found, user is not signed in');
  }

  

// Example: Getting the token from localStorage
// const token = localStorage.getItem('jwt_token');

  if (token) {
      try {
          // const decoded = jwt_decode(token);  // Decodes the JWT token

          // Now you can access the userId from the decoded payload
          // const userId = decoded.user_id;  // Assuming your token has 'user_id'
          console.log("User ID:", userId);
      } catch (error) {
          console.error("Error decoding token:", error);
      }
  } else {
      console.log("No token found");
  }


  try {
    // Send token in the Authorization header
    const response = await fetch('http://127.0.0.1:5000/collab_recommend', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // Include token in the Authorization header
      }
      // You can send an empty object or any other body if needed
    });

    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    const data = await response.json();
    recommendedMovies = data.movies; // Assuming the API returns a list of movies
  } catch (error) {
    errorMessage = error.message;
  }
}


  // Fetch recommendations when the component is mounted
  onMount(() => {
    fetchRecommendations();
  });
</script>

<h2>Collaborative Recommendations</h2>

{#if errorMessage}
  <p style="color: red;">{errorMessage}</p>
{:else if recommendedMovies.length > 0}
  <ul>
    {#each recommendedMovies as movie}
      <li>{movie.title} ({movie.year})</li>
    {/each}
  </ul>
{:else}
  <p>Loading recommendations...</p>
{/if}
