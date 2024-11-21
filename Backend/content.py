
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

def get_recommendations(df, movie_title):
  # Convert the list of genres into a single string for each row
  # df['genres_str'] = df['genres'].apply(lambda x: ' '.join(x))
  # print(df['genres_str'])
  df['genres_str'] = df['genres_str'].astype(str).str.strip()
  df['overview'] = df['overview'].astype(str).str.strip()

  tfidf_genres = TfidfVectorizer()
  genres_matrix = tfidf_genres.fit_transform(df['genres_str'])

  print("stmt1")

  # Vectorize overview (TF-IDF)
  tfidf_overview = TfidfVectorizer(stop_words='english')
  overview_matrix = tfidf_overview.fit_transform(df['overview'])



  print("stmt2")

  weights = {
    
      'genres_str': 0.3205,
      'popularity': 0.2564,
      'vote_average': 0.1923,
      'overview': 0.1923,
      'runtime': 0.0385

  }

  # Fill missing values with placeholders
  df['overview'] = df['overview'].fillna('')
  df['popularity'] = df['popularity'].fillna(0)
  df['vote_average'] = df['vote_average'].fillna(0)
  df['runtime'] = df['runtime'].fillna(0)

  # Normalize numeric columns
  scaler = MinMaxScaler()
  df[['popularity', 'vote_average', 'runtime']] = scaler.fit_transform(df[[ 'popularity', 'vote_average', 'runtime']])


  # Function to calculate weighted similarity
  def weighted_content_recommendation(movie_id, df, weights):
      idx = df[df['id'] == movie_id].index[0]
      
      # Calculate cosine similarity for each feature
      cosine_sim_genres = cosine_similarity(genres_matrix, genres_matrix[idx])
      cosine_sim_overview = cosine_similarity(overview_matrix, overview_matrix[idx])
      cosine_sim_popularity = cosine_similarity(df[['popularity']], df[['popularity']].iloc[idx:idx+1])
      cosine_sim_vote = cosine_similarity(df[['vote_average']], df[['vote_average']].iloc[idx:idx+1])
      cosine_sim_runtime = cosine_similarity(df[['runtime']], df[['runtime']].iloc[idx:idx+1])
      
      # Weighted sum of similarities
      similarity_scores = (
          weights['genres_str'] * cosine_sim_genres.flatten() +
          weights['overview'] * cosine_sim_overview.flatten() +
          weights['popularity'] * cosine_sim_popularity.flatten() +
          weights['vote_average'] * cosine_sim_vote.flatten()  +
          weights['runtime'] * cosine_sim_runtime.flatten()
      )
      
      # Sort and return top recommendations
      df['similarity_score'] = similarity_scores
      recommendations = df.sort_values(by='similarity_score', ascending=False).iloc[1:11]  # Exclude the first result as it will be the movie itself
      return recommendations[['title', 'similarity_score']]

  # Example usage:
  movie_id = df[df['title'] == movie_title]['id'].values[0]
  # movie_id = '862'  # Replace with actual movie ID you want recommendations for
  recommendations = weighted_content_recommendation(movie_id, df, weights)
  print(recommendations)
  return recommendations.to_dict(orient='records')  # Convert to list of dictionaries for JSON response
