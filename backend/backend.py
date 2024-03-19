from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Change this to your preferred database
db = SQLAlchemy(app)

# Define your database models
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Example: User ID who created the recipe
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=True)
    time = db.Column(db.Integer, nullable=False)
    footnotes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Recipe {self.title}>'

# Define your API routes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    output = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'user_id': recipe.user_id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'difficulty': recipe.difficulty,
            'cuisine': recipe.cuisine,
            'tags': recipe.tags,
            'time': recipe.time,
            'footnotes': recipe.footnotes,
        }
        output.append(recipe_data)
    return jsonify({'recipes': output})

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.json
    new_recipe = Recipe(title=data['title'], ingredients=data['ingredients'], instructions=data['instructions'], user_id=data['user_id'])
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe created successfully'}), 201

# You can define additional routes for updating, deleting, or retrieving specific recipes

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  # Set debug=True for development environment
