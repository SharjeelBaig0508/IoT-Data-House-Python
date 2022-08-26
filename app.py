# ---------< Library Imports >---------
from flask import Flask
from flask_cors import CORS
from database_layer import initialize_database

# ---------< Logging Implementation >---------
import app_logger
app_logger.logger_initializer(
    app_name = __name__, 
    logger_name = 'logger', 
    logging_format = '[%(asctime)s] [%(levelname)s] [%(remote_addr)s] requested [%(url)s %(method)s] [%(filename)s:%(lineno)d] in %(module)s" %(message)s with params: %(params)s and body: %(body)s',
    logging_level = 'DEBUG'
)

import global_variables
rootLogger = global_variables.multiprocess_globals['logger']
logger = rootLogger.getChild(__name__)

# ---------< Environment Variables >---------
from os import environ
import dotenv
if dotenv.find_dotenv():
    logger.info("Loaded Environment")
    dotenv.load_dotenv()

# -----------< Flask App Initialization >----------- 
app = Flask(__name__)

# ----------< Cross Origin Implementation >----------
CORS(app)

# ----------< MongoEngine Initialization >----------
app.config['MONGODB_SETTINGS'] = [
    {
        'host': environ.get('DATABASE_URL')
    }
]
initialize_database(app)

# ---------< Run Application >---------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9010, debug=True)
