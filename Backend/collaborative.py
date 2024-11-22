import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to get collaborative filtering recommendations
def get_collab_recommendations(df, user_id, num_recommendations=5):
    """
    Builds a user-based collaborative filtering recommendation system.

    Args:
    - df (pd.DataFrame): DataFrame containing 'userId', 'movieId', and 'rating'.
    - user_id (int): ID of the user for whom recommendations are to be generated.
    - num_recommendations (int): Number of recommendations to return.

    Returns:
    - List[Tuple]: List of recommended movie IDs and predicted ratings.
    """
    # Ensure the DataFrame contains necessary columns
    if not all(col in df.columns for col in ['userId', 'movieId', 'rating']):
        raise ValueError("DataFrame must contain 'userId', 'movieId', and 'rating' columns.")
    
    # Create a user-item matrix
    user_item_matrix = df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # Compute the cosine similarity between users
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Get the user's similarity scores
    user_sim_scores = user_similarity_df.loc[user_id]

    # Get the ratings of all users, weighted by similarity scores
    weighted_ratings = user_item_matrix.T.dot(user_sim_scores)

    # Normalize by the sum of similarity scores
    similarity_sums = user_sim_scores.dot(user_item_matrix > 0)
    predicted_ratings = weighted_ratings / (similarity_sums + 1e-9)  # Avoid division by zero

    # Get the movies the user hasn't rated yet
    rated_movies = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index
    unrated_movies = user_item_matrix.columns.difference(rated_movies)

    # Generate recommendations by predicted rating
    recommendations = predicted_ratings.loc[unrated_movies].sort_values(ascending=False).head(num_recommendations)

    return [(movie_id, predicted_ratings[movie_id]) for movie_id in recommendations.index]

# # # Example Usage
# if __name__ == "__main__":
#     # Load your dataset
    
#     df = pd.read_csv('C:/Users/Deepali/Desktop/RS_Mini/MovieRecommendationSystem/dataset/ratings_small.csv')

#     # Replace with the user ID you want recommendations for
#     user_id = 1
#     recommendations = get_collab_recommendations(df, user_id)
    
#     print(f"Top recommendations for User {user_id}:")
#     for movie, pred_rating in recommendations:
#         print(f"Movie ID: {movie}, Predicted Rating: {pred_rating:.2f}")
