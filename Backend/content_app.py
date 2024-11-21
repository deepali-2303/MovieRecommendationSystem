from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
import pandas as pd
from content import get_recommendations  # Function from your notebook
from flask_cors import CORS

# Initialize Flask app, CORS, Bcrypt, and SQLAlchemy
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Set users.db as the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Set up database connection for movies
engine = create_engine('sqlite:///movies.db')  # Set movies.db as the database for movie data

# User Model for signup and login
class User(db.Model):
    __tablename__ = 'users'  # This specifies the table name as 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create tables for the 'users' database
with app.app_context():
    db.create_all()

# Route for signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the username or email already exists
    user = User.query.filter((User.username == username) | (User.email == email)).first()
    if user:
        return jsonify({"error": "Username or email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create and add user to the database
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Find user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Check if the password is correct
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200


# Existing routes for movies
@app.route('/movies', methods=['GET'])
def get_movies():
    with engine.connect() as conn:
        df = pd.read_sql('SELECT title FROM movies', conn)
    return jsonify(df['title'].tolist())


@app.route('/top_movies', methods=['GET'])
def get_top_movies():
    with engine.connect() as conn:
        df = pd.read_sql('SELECT title, vote_average FROM movies', conn)
    top_movies = df.sort_values(by='vote_average', ascending=False).head(10)
    return jsonify(top_movies.to_dict(orient='records'))


@app.route('/recommend', methods=['GET'])
def recommend():
    movie_title = request.args.get('title')
    with engine.connect() as conn:
        df = pd.read_sql('SELECT * FROM movies', conn)
    recommendations = get_recommendations(df, movie_title)
    return jsonify(recommendations)


@app.route('/movie_info', methods=['GET'])
def get_movie_info():
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "No movie title provided"}), 400

    with engine.connect() as conn:
        query = f"SELECT * FROM movies WHERE title = '{movie_title}'"
        df = pd.read_sql(query, conn)

    if df.empty:
        return jsonify({"error": "Movie not found"}), 404

    movie_info = df.to_dict(orient='records')[0]
    return jsonify(movie_info)


if __name__ == '__main__':
    app.run(debug=True)
