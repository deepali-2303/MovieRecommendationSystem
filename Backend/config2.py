# from sqlalchemy import create_engine
# import pandas as pd

# # Step 1: Connect to the combined database (movies and ratings)
# engine_combined = create_engine('sqlite:///combined.db')

# # Step 2: Read movies and ratings data from the combined database
# movies_df = pd.read_sql('SELECT * FROM movies', engine_combined)
# ratings_df = pd.read_sql('SELECT * FROM ratings', engine_combined)

# # Step 3: Connect to the users database
# engine_users = create_engine('sqlite:///users.db')

# # Step 4: Read users data from the users database
# users_df = pd.read_sql('SELECT * FROM users', engine_users)

# # Step 5: Merge ratings and users based on userId
# ratings_with_users_df = pd.merge(ratings_df, users_df, left_on='userId', right_on='id', how='inner')

# # Step 6: Merge the result with movies based on movieId
# final_combined_df = pd.merge(ratings_with_users_df, movies_df, left_on='movieId', right_on='id', how='inner')

# # Step 7: Connect to the combined database again to update it
# final_db_engine = create_engine('sqlite:///combined.db')

# # Step 8: Write the final combined data back to the movies database (or you can choose another table name)
# final_combined_df.to_sql('movies', final_db_engine, if_exists='replace', index=False)

# print('Movies database successfully updated with ratings and user data!')




import sqlite3
import pandas as pd

# Path to your CSV file
csv_file = 'C:/Users/Deepali/Desktop/RS_Mini/MovieRecommendationSystem/dataset/movies_metadata_cleaned.csv'

# Name of the SQLite database
db_name = 'movies.db'

# Name of the table in the SQLite database
table_name = 'movies'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Establish a connection to SQLite database (creates the database if it doesn't exist)
conn = sqlite3.connect(db_name)

# Export the DataFrame to SQLite database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Verify data insertion
print(f"Data successfully imported into the '{table_name}' table of '{db_name}' database.")

# Close the database connection
conn.close()
