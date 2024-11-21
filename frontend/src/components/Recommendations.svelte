<script>
  export let selectedMovie;
  export let recommendations;

  // console.log('Selected Movie:', selectedMovie);
  // console.log('Recommendations:', recommendations);
</script>

<style>
  .recommendations {
    margin-top: 20px;
  }
  .recommendation-item {
    padding: 8px;
    border: 1px solid #ccc;
    margin-bottom: 5px;
  }
  .no-recommendations {
    color: #999;
  }
</style>

<div class="recommendations">
  <h3>Recommendations for {selectedMovie ? selectedMovie : 'Movie'}</h3>
  <ul>
    {#if recommendations && recommendations.length > 0}
      {#each recommendations as recommendation (recommendation.title)}
        <li class="recommendation-item">
          {#if recommendation.title && recommendation.similarity_score !== undefined}
            {recommendation.title} (Score: {recommendation.similarity_score.toFixed(2)})
          {:else}
            <span class="no-recommendations">No valid data available</span>
          {/if}
        </li>
      {/each}
    {:else}
      <li class="no-recommendations">No recommendations available</li>
    {/if}
  </ul>
</div>
