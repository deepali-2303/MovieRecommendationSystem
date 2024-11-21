from sqlalchemy import create_engine
import pandas as pd

# Step 1: Connect to the combined database (movies and ratings)
engine_combined = create_engine('sqlite:///combined.db')

# Step 2: Read movies and ratings data from the combined database
movies_df = pd.read_sql('SELECT * FROM movies', engine_combined)
ratings_df = pd.read_sql('SELECT * FROM ratings', engine_combined)

# Step 3: Connect to the users database
engine_users = create_engine('sqlite:///users.db')

# Step 4: Read users data from the users database
users_df = pd.read_sql('SELECT * FROM users', engine_users)

# Step 5: Merge ratings and users based on userId
ratings_with_users_df = pd.merge(ratings_df, users_df, left_on='userId', right_on='id', how='inner')

# Step 6: Merge the result with movies based on movieId
final_combined_df = pd.merge(ratings_with_users_df, movies_df, left_on='movieId', right_on='id', how='inner')

# Step 7: Connect to the combined database again to update it
final_db_engine = create_engine('sqlite:///combined.db')

# Step 8: Write the final combined data back to the movies database (or you can choose another table name)
final_combined_df.to_sql('movies', final_db_engine, if_exists='replace', index=False)

print('Movies database successfully updated with ratings and user data!')
