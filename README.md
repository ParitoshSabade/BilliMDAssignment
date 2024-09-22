# User Management API

This project implements a User Management API with signup, login, logout, and update functionalities using Flask and MongoDB.

## Project Structure

- `requirements.txt`: Lists all Python dependencies for the project.
- `schemas.py`: Contains JSON schemas for request validation.
- `models.py`: Defines the User model with helper methods.
- `app.py`: Main application file with API endpoints and business logic.

## Setup

### Prerequisites

1. MongoDB server running locally or remotely.
2. Python 3.7+

### Environment Setup

1. Create a `.env.development` file in the project root. Sample file given below:

MONGO_URI=mongodb://localhost:27017
DB_NAME=UserDatabase
COLLECTION_NAME=User
JWT_SECRET_KEY=your_jwt_secret_key
SESSION_SECRET_KEY=your_session_secret_key

Replace the values with your actual MongoDB URI, database name, collection name, and secret keys.

2. Create the required database and collection in MongoDB before running the application.

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:
pip install -r requirements.txt


## Running the Application

Start the Flask server:
python app.py


The server will run on `http://localhost:8000`.

## API Testing

For testing the API, follow this sequence of calls:

1. Signup
2. Login
3. Update

### Sample cURL Commands

#### Signup (POST)
curl --location 'http://localhost:8000/signup'
--header 'Content-Type: application/json'
--data '{
"first_name": "John",
"middle_name": "Doe",
"last_name": "Smith",
"password": "securepassword123",
"phone": "1234567890"
}'


#### Login (POST)
curl --location 'http://localhost:8000/login'
--header 'Content-Type: application/json'
--data '{
"phone": "1234567890",
"password": "securepassword123"
}'
Use phone and password used to signup.

#### Update (PUT)
curl --location --request PUT 'http://localhost:8000/user'
--header 'Authorization: <jwt_token_from_login>'
--header 'Session-Token: <session_token_from_login>'
--header 'Content-Type: application/json'
--data '{
"_id": {"$oid": "<user_id_from_signup>"},
"last_name": "Smith"
}'


Replace `<jwt_token_from_login>`, `<session_token_from_login>`, and `<user_id_from_signup>` with the actual values obtained from the signup and login responses.

## Security Features

- Passwords are hashed before storage in the database.
- JWT and session token-based authentication.
- Input validation using JSON schemas.
- Error handling.
