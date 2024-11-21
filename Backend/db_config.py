from sqlalchemy import create_engine
import pandas as pd

# Load the datasets
df = pd.read_csv('C:/Users/Deepali/Desktop/RS_Mini/MovieRecommendationSystem/dataset/movies_metadata_cleaned.csv')  
df2 = pd.read_csv('C:/Users/Deepali/Desktop/RS_Mini/MovieRecommendationSystem/dataset/ratings_small.csv')

# Initialize the SQLite engine
engine = create_engine('sqlite:///combined.db')

# Write the movies data to the database
df.to_sql('movies', engine, if_exists='replace', index=False)

# Write the ratings data to the database
df2.to_sql('ratings', engine, if_exists='replace', index=False)

# Perform a SQL query to join both tables on MovieId
query = """
SELECT m.*, r.*
FROM movies m
JOIN ratings r ON m.id = r.movieId
"""
# Read the results of the join into a DataFrame
combined_df = pd.read_sql(query, engine)

# Print the first few rows of the combined DataFrame
print(combined_df.head())

print('Database created and tables linked successfully!')
