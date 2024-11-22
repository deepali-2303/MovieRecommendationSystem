from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
import pandas as pd
from content import get_recommendations  # Function from your notebook
from flask_cors import CORS
from collaborative import get_collab_recommendations  # Function from your notebook
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Initialize Flask app, CORS, Bcrypt, and SQLAlchemy
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Set users.db as the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# JWT secret and expiration settings
JWT_SECRET = 'your_jwt_secret_key'  # Replace with a secure key
JWT_EXPIRATION = 24  # Token expiration in hours

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Set up database connection for movies
engine = create_engine('sqlite:///movies.db')  # Set movies.db as the database for movie data
engine_ratings = create_engine('sqlite:///ratings.db')  # Set ratings.db as the database for ratings data

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

# JWT verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get the Authorization header
        if not token:
            return jsonify({"error": "Token is missing"}), 403

        try:
            token = token.split(" ")[1]  # Extract the token part from "Bearer <token>"
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            kwargs['user_id'] = data['user_id']  # Extract user_id from token's payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


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
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION)
    }, JWT_SECRET, algorithm='HS256')


    return jsonify({"message": "Login successful", "token": token}), 200

# Existing routes for movies
@app.route('/movies', methods=['GET'])
@token_required
def get_movies():
    with engine.connect() as conn:
        df = pd.read_sql('SELECT title FROM movies', conn)
    return jsonify(df['title'].tolist())

@app.route('/top_movies', methods=['GET'])
# @token_required
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

@app.route('/collab_recommend', methods=['GET'])
@token_required
def collab(user_id):
    with engine_ratings.connect() as conn:
        query = f"SELECT * FROM ratings"
        df2 = pd.read_sql(query, conn)

    recommendations = get_collab_recommendations(df2, user_id)
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
