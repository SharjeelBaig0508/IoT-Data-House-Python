# Library Imports
from flask import Flask
from database_layer import initialize_database
from os import environ
import dotenv
if dotenv.find_dotenv():
    dotenv.load_dotenv()

# Flask App Initialization
app = Flask(__name__)

# MongoEngine Initialization
app.config['MONGODB_SETTINGS'] = [
    {
        'host': environ.get('DATABASE_URL')
    }
]
initialize_database(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9010, debug=True)
