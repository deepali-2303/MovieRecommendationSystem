import MovieList from '../components/MovieList.svelte';
import Recommendations from '../components/Recommendations.svelte';

export const routes = {
    '/': MovieList,
    '/recommendations/:movie': Recommendations
};