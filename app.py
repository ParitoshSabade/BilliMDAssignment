from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from pymongo import MongoClient, errors
from bson import ObjectId
from dotenv import load_dotenv
import os
from models import User
from schemas import user_update_schema  # Import the schema

load_dotenv('.env.development')

app = Flask(__name__)
schema = JsonSchema(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
user_collection = db[os.getenv('COLLECTION_NAME')]


def check_authorization():
    auth = request.authorization
    session_token = request.headers.get('Session-Token')
    if not auth or not session_token:
        return False, "Missing Authorization or session_token"
    if auth.password != os.getenv('BEARER_TOKEN'):
        return False, "Invalid Authorization Token"
    return True, "Authorized"

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({'Status': 'failure', 'reason': e.message}), 400

@app.route('/user', methods=['PUT'])
@schema.validate(user_update_schema)  # Use the imported schema
def update_user():
    try:
        auth_valid, auth_msg = check_authorization()
        if not auth_valid:
            return jsonify({"Status": "failure", "reason": auth_msg}), 401

        if not db.name in client.list_database_names():
            return jsonify({"Status": "failure", "reason": "Database not found"}), 404

        if not user_collection.name in db.list_collection_names():
            return jsonify({"Status": "failure", "reason": "Collection not found"}), 404
        
        data = request.get_json()
        user_id = ObjectId(data[User.USER_ID])
        user_in_db = user_collection.find_one({"_id": user_id})

        if not user_in_db:
            return jsonify({"Status": "failure", "reason": "User not found"}), 404
        
        session_token = request.headers.get('Session-Token')
        if user_in_db['session_token'] != session_token:
            return jsonify({"Status": "failure", "reason": "Invalid session token"}), 498


        user = User(data)
        update_data = user.to_update_dict()

        user_collection.update_one({"_id": user_id}, {"$set": update_data})

        return jsonify({"Status": "success", "reason": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)