from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt

app = Flask(__name__)
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
            data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated_function


# Define your API routes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = list(recipes_collection.find({}))  # Retrieve all recipes from the collection
    return jsonify({'recipes': recipes})

@app.route('/recipes', methods=['POST'])
@token_required
def create_recipe():
    data = request.json
    new_recipe = {
        'title': data['title'],
        'user_id': data['user_id'],
        'date_posted': data['data_posted'],
        'description': data['description'],
        'difficulty': data['difficulty'],
        'cuisine': data['cuisine'],
        'ingredients': data['ingredients'],
        'instructions': data['instructions'],
        'tags': data['tags'],
        'time_posted': data['time_posted'],
        'footnotes': data['footnotes'],
        'likes': data['likes'],
        'photos': data['photos']
    }
    recipes_collection.insert_one(new_recipe)  # Insert the new recipe document into the collection
    return jsonify({'message': 'Recipe created successfully'}), 201


# You can define additional routes for updating, deleting, or retrieving specific recipes

if __name__ == '__main__':
    app.run(debug=True)
