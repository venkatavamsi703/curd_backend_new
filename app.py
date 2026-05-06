from flask import Flask, request, jsonify
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# ROOT ROUTE
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "CRUD API is running", "endpoints": {
        "create": "POST /users",
        "read": "GET /users",
        "update": "PUT /users/<id>",
        "delete": "DELETE /users/<id>"
    }})

# CREATE
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    db.collection('users').add({
        'name': data['name'],
        'email': data['email']
    })

    return jsonify({"message": "User added to Firebase"})

# READ
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    docs = db.collection('users').stream()

    for doc in docs:
        user = doc.to_dict()
        user['id'] = doc.id
        users.append(user)

    return jsonify(users)

# UPDATE
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json

    db.collection('users').document(id).update({
        'name': data['name'],
        'email': data['email']
    })

    return jsonify({"message": "User updated"})

# DELETE
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.collection('users').document(id).delete()

    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)