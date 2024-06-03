from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId, json_util
from dotenv import load_dotenv
import json
import jwt
import datetime
import hashlib
from flask_cors import CORS # type: ignore
import requests
import os
import base64
from google.cloud import storage


# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'BabyCakes123'
connection_string = "mongodb+srv://recipeAdmin:8YyKQeylo6z3lnH8@recipe-database.e0pj4aj.mongodb.net/?retryWrites=true&w=majority&appName=recipe-database"
client = MongoClient(connection_string)  # Connect to MongoDB (adjust URI as needed)
db = client['recipe_database']  # Connect to your MongoDB database

# Define your MongoDB collection
recipes_collection = db['recipes']
users_collection = db['users']
travel_collection = db['travel']

curr_spotify_token_harry = ""
curr_spotify_token_katie = ""
bucket_name = "app-travel-photos"

google_storage_client = storage.Client.from_service_account_json(os.environ.get('GOOGLE_STORAGE_PATH'))

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
    id = request.args.get('id', type=str)
    if not id:
        recipes = list(recipes_collection.find())
        return json.loads(json_util.dumps(recipes))
    else:
        object_id = ObjectId(id)
        recipe = recipes_collection.find_one({'_id': object_id})
        if recipe is None:
            errorStr = f'Recipe with _id: {id} not found'
            return jsonify({'Error': errorStr}), 404
        else:
            return json.loads(json_util.dumps(recipe))

# Add a new recipe to database
@token_required
@app.route('/recipe', methods=['POST'])
def create_recipe():
    data = request.json
    new_recipe = {
        'title': data['title'],
        # 'user_id': data['user_id'],
        'date_posted': datetime.datetime.now().isoformat(),
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
def refresh_token(isHarry):
    url = "https://accounts.spotify.com/api/token"
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    if (isHarry is True):
        refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN_HARRY')
    else:
        refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN_KATIE')
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
    # Get track data for Harry
    global curr_spotify_token_harry;
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=5"
    headers = {
    'Authorization': f'Bearer {curr_spotify_token_harry}',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    track_response = requests.get(url, headers=headers)
    if (track_response.status_code == 200):
        track_data_harry = track_response.json()
    else:
        curr_spotify_token_harry = refresh_token(True);
        headers = {
            'Authorization': f'Bearer {curr_spotify_token_harry}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        track_response = requests.get(url, headers=headers)
        track_data_harry = track_response.json()
    
    # Get Artist data for harry
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=5"
    artist_response = requests.get(url, headers=headers)
    artist_data_harry = artist_response.json()
    
    # Get track data for Katie
    global curr_spotify_token_katie;
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=5"
    headers = {
    'Authorization': f'Bearer {curr_spotify_token_katie}',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    track_response = requests.get(url, headers=headers)
    if (track_response.status_code == 200):
        track_data_katie = track_response.json()
    else:
        curr_spotify_token_katie = refresh_token(False);
        headers = {
            'Authorization': f'Bearer {curr_spotify_token_katie}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        track_response = requests.get(url, headers=headers)
        track_data_katie = track_response.json()
    # Get Artist data
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=5"
    artist_response = requests.get(url, headers=headers)
    artist_data_katie = artist_response.json()
    return jsonify({"harry": {"track_data": track_data_harry, "artist_data": artist_data_harry},
                    "katie": {"track_data": track_data_katie, "artist_data": artist_data_katie}}), 200

# Add photos to Google Cloud object storage
@token_required
@app.route('/upload_photo', methods=['POST'])
def get_signed_url():
    file = request.args.get('file', type=str)
    country = request.args.get('country', type=str)
    region = request.args.get('region', type=str)
    city = request.args.get('city', type=str)
    if region:
        name = f"{country}\\{region}\\{city}\\{file}"
    else:
        name = f"{country}\\{city}\\{file}"
        
    # Create a storage client using the credentials
    global google_storage_client
    global bucket_name
    bucket = google_storage_client.bucket(bucket_name)
    blob = bucket.blob(name)
    signed_url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=10),
        # Allow PUT requests using this URL.
        method="PUT",
        content_type="application/octet-stream",
    )
    return jsonify({signed_url}), 200

# Fetch objects (photos) related to the country + region + town
@app.route('/travel/photos', methods=['GET'])
def fetch_objects():
    country = request.args.get('country', type=str)
    region = request.args.get('region', type=str)
    city = request.args.get('city', type=str)
    
    # Create a storage client using the credentials
    global google_storage_client
    global bucket_name
    if region:
        prefix = f"{country}_{region}_{city}"
    else:
        prefix = f"{country}_{city}"
    print(f"Prefix = {prefix}")
    blobs = google_storage_client.list_blobs(bucket_name, prefix=prefix, delimiter='/')
    photos = []
    for blob in blobs:
        photos.append(f"https://storage.cloud.google.com/{bucket_name}/{blob.name}")
    return jsonify({"photos": photos}), 200

# Fetch everything from the 'travel' collection in mongoDB that matches the country
@app.route('/travel', methods=['GET'])
def fetch_country_documents():
    country = request.args.get('country', type=str)
    if not country:
        return jsonify({"error": "invalid country"}), 404
    
    # Query the collection
    query = {"country": country}
    documents = travel_collection.find(query)
    
    if not documents:
        return jsonify({"error": "invalid country"}), 404
    
    document_array = []
    print("Documents")
    for document in documents:
        del document['_id']
        print(document)
        document_array.append(document)
    return jsonify({"documents": document_array}), 200
    

if __name__ == '__main__':
    app.run(debug=True)
