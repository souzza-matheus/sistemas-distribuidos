from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})

# Configure MongoDB connection
client = MongoClient('mongodb://admin:12345678@localhost:27017/')
db = client['test']
collection = db['pessoas']

# CLI routes
@app.route('/cli/add_person', methods=['POST'])
def cli_add_person():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    
    # Insert the person into MongoDB
    person = {'nome': nome, 'email': email}
    collection.insert_one(person)
    
    return jsonify({'message': 'Person added successfully'})

@app.route('/cli/list_people', methods=['GET'])
def cli_list_people():
    people = list(collection.find({}, {'_id': 0, 'nome': 1, 'email': 1}))  # Include 'nome' and 'email' fields only
    return jsonify(people)

@app.route('/cli/update_person/<name>', methods=['PUT'])
def cli_update_person(name):
    data = request.get_json()
    new_email = data.get('email')
    
    # Update the person in MongoDB
    collection.update_one({'name': name}, {'$set': {'email': new_email}})
    
    return jsonify({'message': f'Person {name} updated successfully'})

@app.route('/cli/delete_person/<name>', methods=['DELETE'])
def cli_delete_person(name):
    # Delete the person from MongoDB
    collection.delete_one({'name': name})
    
    return jsonify({'message': f'Person {name} deleted successfully'})

# HTML routes
@cross_origin()
@app.route('/')
def index():
    return render_template('index.html')

@cross_origin()
@app.route('/add_person', methods=['POST'])
def add_person():
    nome = request.form.get('nome')
    email = request.form.get('email')
    
    # Insert the person into MongoDB
    person = {'nome': nome, 'email': email}
    collection.insert_one(person)
    
    return 'Person added successfully'

@cross_origin()
@app.route('/list_people', methods=['GET'])
def list_people():
    people = list(collection.find({}, {'_id': 0}))
    return jsonify(people)
@cross_origin()
@app.route('/update_person/<name>', methods=['POST'])
def update_person(name):
    new_email = request.form.get('email')
    
    # Update the person in MongoDB
    collection.update_one({'nome': name}, {'$set': {'email': new_email}})
    
    return f'Person {name} updated successfully'

@cross_origin()
@app.route('/delete_person/<name>', methods=['GET', 'POST'])
def delete_person(name):
    if request.method == 'POST':
        # Delete the person from MongoDB
        collection.delete_one({'nome': name})
        return f'Person {name} deleted successfully'
    else:
        return f'Person {name} deleted successfully'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)