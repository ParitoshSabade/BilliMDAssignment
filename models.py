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
    def hash_password(password):
        if password:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return None

    def to_update_dict(self):
        update_dict = {}
        for key, value in self.data.items():
            if key == User.PASSWORD:
                update_dict[key] = self.hash_password(value)
            elif key == User.UPDATED_DATETIME:
                update_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            elif key in User.allowed_update_fields:
                update_dict[key] = value
        return update_dict