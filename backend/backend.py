from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BabyCakes123'
connection_string = "mongodb+srv://recipeAdmin:8YyKQeylo6z3lnH8@recipe-database.e0pj4aj.mongodb.net/?retryWrites=true&w=majority&appName=recipe-database"
client = MongoClient(connection_string)  # Connect to MongoDB (adjust URI as needed)
db = client['recipe_database']  # Connect to your MongoDB database

# Define your MongoDB collection
recipes_collection = db['recipes']

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

    # check mongoDB database
    # if username not in users or users[username] != password:
    #     return jsonify({'message': 'Invalid credentials'}), 401

    # Generate JWT token
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)  # Token expiration time
    }, app.config['SECRET_KEY'])
    return jsonify({'token': token}), 200

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
@app.route('/recipes', methods=['POST'])
@token_required
def create_recipe():
    data = request.json
    new_recipe = {
        'title': data['title'],
        'user_id': data['user_id'],
        'date_posted': data['date_posted'],
        'description': data['description'],
        'difficulty': data['difficulty'],
        'cuisine': data['cuisine'],
        'ingredients': data['ingredients'],
        'instructions': data['instructions'],
        'tags': data['tags'],
        'footnotes': data['footnotes'],
        'likes': data['likes'],
        'photos': data['photos']
    }
    recipes_collection.insert_one(new_recipe)  # Insert the new recipe document into the collection
    return jsonify({'message': 'Recipe created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
