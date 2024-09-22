from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from pymongo import MongoClient, errors
from bson import ObjectId
from dotenv import load_dotenv
import os
from models import User
from schemas import user_update_schema, user_signup_schema, user_login_schema
import jwt
from functools import wraps

load_dotenv('.env.development')

app = Flask(__name__)
schema = JsonSchema(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
user_collection = db[os.getenv('COLLECTION_NAME')]

db_name = os.getenv('DB_NAME')
if db_name not in client.list_database_names():
    raise Exception(f"Database '{db_name}' does not exist")

collection_name = os.getenv('COLLECTION_NAME')
if collection_name not in db.list_collection_names():
    raise Exception(f"Collection '{collection_name}' does not exist")

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Status': 'failure', 'reason': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = user_collection.find_one({"_id": ObjectId(data['_id'])})
            if not current_user:
                return jsonify({'Status': 'failure', 'reason': 'User not found'}), 401
        except:
            return jsonify({'Status': 'failure', 'reason': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'Status': 'failure', 'reason': e.message}), 400

@app.route('/signup', methods=['POST'])
@schema.validate(user_signup_schema)
def signup():
    try:
        data = request.get_json()
        user = User(data)
        user_data = user.to_dict()
        
        existing_user = user_collection.find_one({"phone": user_data['phone']})
        if existing_user:
            return jsonify({"Status": "failure", "reason": "User with this phone number already exists"}), 409
        
        result = user_collection.insert_one(user_data)
        return jsonify({"Status": "success", "reason": "User created successfully", "_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

@app.route('/login', methods=['POST'])
@schema.validate(user_login_schema)
def login():
    try:
        data = request.get_json()
        user = user_collection.find_one({"phone": data['phone']})
        if user and User.check_password(data['password'], user['password']):
            token = jwt.encode({'_id': str(user['_id'])}, JWT_SECRET_KEY, algorithm="HS256")
            session_token = User.generate_session_token()
            user_collection.update_one({"_id": user['_id']}, {"$set": {"session_token": session_token}})
            return jsonify({"Status": "success", "token": token, "session_token": session_token}), 200
        return jsonify({"Status": "failure", "reason": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    try:
        user_collection.update_one({"_id": current_user['_id']}, {"$unset": {"session_token": ""}})
        return jsonify({"Status": "success", "reason": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

@app.route('/user', methods=['PUT'])
@schema.validate(user_update_schema)
@token_required
def update_user(current_user):
    try:
        data = request.get_json()
        _id = data[User.USER_ID]['$oid']
        
        if str(current_user['_id']) != _id:
            return jsonify({"Status": "failure", "reason": "Unauthorized to update this user"}), 403
        
        session_token = request.headers.get('Session-Token')
        if current_user['session_token'] != session_token:
            return jsonify({"Status": "failure", "reason": "Invalid session token"}), 498

        user = User(data)
        update_data = user.to_update_dict()

        user_collection.update_one({"_id": ObjectId(_id)}, {"$set": update_data})

        return jsonify({"Status": "success", "reason": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)