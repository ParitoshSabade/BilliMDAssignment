from bson import ObjectId
from datetime import datetime
import bcrypt
import uuid

class User:
    USER_ID = '_id'
    FIRST_NAME = 'first_name'
    MIDDLE_NAME = 'middle_name'
    LAST_NAME = 'last_name'
    PASSWORD = 'password'
    PHONE = 'phone'
    CREATED_DATETIME = 'created_datetime'
    UPDATED_DATETIME = 'updated_datetime'
    SESSION_TOKEN = 'session_token'

    allowed_update_fields = [FIRST_NAME, MIDDLE_NAME, LAST_NAME, PASSWORD, PHONE, UPDATED_DATETIME]

    def __init__(self, data):
        self.data = data

    @staticmethod
    def hash_password(password):
        if password:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return None

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def generate_session_token():
        return str(uuid.uuid4())

    def to_dict(self):
        return {
            self.FIRST_NAME: self.data.get(self.FIRST_NAME),
            self.MIDDLE_NAME: self.data.get(self.MIDDLE_NAME),
            self.LAST_NAME: self.data.get(self.LAST_NAME),
            self.PHONE: self.data.get(self.PHONE),
            self.PASSWORD: self.hash_password(self.data.get(self.PASSWORD)),
            self.CREATED_DATETIME: datetime.utcnow(),
            self.UPDATED_DATETIME: datetime.utcnow(),
            self.SESSION_TOKEN: self.generate_session_token()
        }

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