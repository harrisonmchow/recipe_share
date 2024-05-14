from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask_cors import CORS # type: ignore
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'BabyCakes123'
connection_string = "mongodb+srv://recipeAdmin:8YyKQeylo6z3lnH8@recipe-database.e0pj4aj.mongodb.net/?retryWrites=true&w=majority&appName=recipe-database"
client = MongoClient(connection_string)  # Connect to MongoDB (adjust URI as needed)
db = client['recipe_database']  # Connect to your MongoDB database

# Define your MongoDB collection
recipes_collection = db['recipes']
users_collection = db['users']

curr_spotify_token = ""

def token_required(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # Extract the token value from the "Authorization" header (e.g., "Bearer <token>")
            token = token.split(' ')[1]
            # Verify the token using a secret key (replace 'your_secret_key' with your actual secret key)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function

### Admin User
@app.route('/login', methods=['POST'])
def login():
    # auth = request.authorization
    auth = request.json
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({'message': 'Invalid credentials'}), 401

    username = auth['username']
    password = auth['password']
    # Create a SHA-256 hash object, convert the password to bytes and hash it
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()

    # check mongoDB database
    user_document = users_collection.find_one({'username': username})
    if not user_document or user_document['password'] != hash_password:
        print(f"Invalid user {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate JWT token
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)  # Token expiration time
    }, app.config['SECRET_KEY'])
    print(f"Successful user login for {username}")
    return jsonify({'token': token}), 200

### Validate token
@app.route('/validate_token', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if token_is_valid(token):
        return jsonify({'valid': True}), 200
    else:
        return jsonify({'valid': False}), 200

def token_is_valid(token):
    if not token:
        return False
    try:    
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(data['exp'])
        print(datetime.datetime.now())
        if datetime.datetime.fromtimestamp(data['exp']) < datetime.datetime.now():
            return False
        return True
    except:
        return False

# Get recipe data
@app.route('/recipes', methods=['GET'])
def get_recipes():
    page_number = request.args.get('page', type=int)
    page_size = request.args.get('page_size', type=int)
    skip = (page_number - 1) * page_size
    skip = max(skip, 0)
    recipes = list(recipes_collection.find({"skip": skip, "limit": page_number}))  # Retrieve all recipes from the collection
    return jsonify({'recipes': recipes})

# Add a new recipe to database
@app.route('/recipe', methods=['POST'])
@token_required
def create_recipe():
    data = request.json
    new_recipe = {
        'title': data['title'],
        # 'user_id': data['user_id'],
        'date_posted': datetime.datetime.now(),
        'description': data['description'],
        'difficulty': data['difficulty'],
        'cuisine': data['cuisine'],
        'ingredients': data['ingredients'],
        'instructions': data['instructions'],
        # 'tags': data['tags'],
        'notes': data['notes'],
        'link': data['link'],
        # 'likes': data['likes'],
        # 'photos': data['photos']
    }
    recipes_collection.insert_one(new_recipe)  # Insert the new recipe document into the collection
    return jsonify({'message': 'Recipe created successfully'}), 201

# Callback function for spotify
@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code', type=str)
    state = request.args.get('state', type=str)
    return jsonify({'code': code, 'state': state}), 200

# Refresh function
def refresh_token():
    url = "https://accounts.spotify.com/api/token"
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')
    payload = f'grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}'
    text = f"{client_id}:{os.environ.get('SPOTIFY_CLIENT_SECRET')}"
    basic_authorization = base64.b64encode(text.encode('utf-8'))
    headers = {
    'Authorization': f'Basic {basic_authorization.decode('utf-8')}',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    track_response = requests.post(url, headers=headers, data=payload)
    data = track_response.json()
    return data['access_token']


@app.route('/spotify_stats', methods=['GET'])
def get_spotify_stats():
    # Get track data
    global curr_spotify_token;
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=5"
    headers = {
    'Authorization': f'Bearer {curr_spotify_token}',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    track_response = requests.get(url, headers=headers)
    if (track_response.status_code == 200):
        data = track_response.json()
    else:
        curr_spotify_token = refresh_token();
        headers = {
            'Authorization': f'Bearer {curr_spotify_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        track_response = requests.get(url, headers=headers)
        data = track_response.json()
    
    # Get Artist data
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=5"
    artist_response = requests.get(url, headers=headers)
    artist_data = artist_response.json()
    return jsonify({"track_data": data, "artist_data": artist_data}), 200

if __name__ == '__main__':
    app.run(debug=True)
