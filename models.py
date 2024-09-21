from bson import ObjectId
from datetime import datetime
import bcrypt

class User:
    
    USER_ID = 'user_id'
    FIRST_NAME = 'first_name'
    MIDDLE_NAME = 'middle_name'
    LAST_NAME = 'last_name'
    PASSWORD = 'password'
    PHONE = 'phone'
    UPDATED_DATETIME = 'updated_datetime'

    allowed_update_fields = [FIRST_NAME, MIDDLE_NAME, LAST_NAME, PASSWORD, PHONE, UPDATED_DATETIME]

    def __init__(self, data):
        self.data = data

    @staticmethod
    def validate_request(data):
        
        if not data.get(User.USER_ID):
            return False, "Missing required field: user_id"
        try:
            ObjectId(data[User.USER_ID])  # Validate user_id is a valid ObjectId
        except Exception as e:
            return False, f"Invalid user_id: {str(e)}"

        
        for key in data.keys():
            if key != User.USER_ID and key not in User.allowed_update_fields:
                return False, f"Invalid field: {key}"
        if User.PASSWORD in data and len(data[User.PASSWORD]) < 8:  
            return False, "Password must be at least 8 characters long"  

        
        if User.UPDATED_DATETIME in data:
            try:
                datetime.strptime(data[User.UPDATED_DATETIME], "%Y-%m-%dT%H:%M:%S.%fZ")  
            except ValueError:  
                return False, "Invalid date format for updated_datetime. Expected format: YYYY-MM-DDTHH:MM:SS.sssZ"  

        return True, "Valid data"

    @staticmethod
    def hash_password(password):
        if password:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return None

    def to_update_dict(self):
        
        update_dict = {}

        for key, value in self.data.items():
            if key == User.PASSWORD:  # Hash password if provided
                update_dict[key] = self.hash_password(value)
            elif key == User.UPDATED_DATETIME:  
                update_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            elif key in User.allowed_update_fields:
                update_dict[key] = value


        return update_dict
