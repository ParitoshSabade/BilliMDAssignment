from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
from models import User
import datetime
import json


load_dotenv('.env.development')

app = Flask(__name__)


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


@app.route('/user', methods=['PUT'])
def update_user():
    
    try:
        
        auth_valid, auth_msg = check_authorization()
        if not auth_valid:
            return jsonify({"Status": "failure", "reason": auth_msg}), 401

        data = request.get_json()

        is_valid, validation_msg = User.validate_request(data)
        if not is_valid:
            return jsonify({"Status": "failure", "reason": validation_msg}), 400

        
        user_id = ObjectId(data[User.USER_ID])
        user_in_db = user_collection.find_one({"_id": user_id})

        session_token = request.headers.get('Session-Token')
        if user_in_db['session_token'] != session_token:
            return jsonify({"Status": "failure", "reason": "Invalid session token"}), 498

        if not user_in_db:
            return jsonify({"Status": "failure", "reason": "User not found"}), 404

        
        user = User(data)
        update_data = user.to_update_dict()

        
        user_collection.update_one({"_id": user_id}, {"$set": update_data})

        return jsonify({"Status": "success", "reason": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"Status": "failure", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000,debug=True)

