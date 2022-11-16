# -------------------------------------< Environment Variables >-------------------------------------
from os import environ
import dotenv
if dotenv.find_dotenv():
    dotenv.load_dotenv()

# -------------------------------------< Logging Implementation >------------------------------------
import app_logger
from logging import Logger
app_logger.logger_initializer(
    app_name = __name__, 
    logger_name = environ.get('LOGGER_NAME'), 
    logging_format = '[%(asctime)s] [%(levelname)s] [%(remote_addr)s] [%(url)s %(method)s] [%(filename)s:%(lineno)d] [PARAMS] %(params)s [BODY] %(body)s [MESSAGE] %(message)s',
    logging_level = environ.get('LOGGER_LEVEL')
)

rootLogger: Logger = app_logger.multi_loggers.get(environ.get('LOGGER_NAME'))
if rootLogger:
    logger = rootLogger.getChild(__name__)

# ----------------------------------------< Library Imports >----------------------------------------
from flask import Flask
from flask_cors import CORS
from mongoengine import ValidationError
from database_layer import initialize_database

# -----------------------------------< Flask App Initialization >------------------------------------ 
app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'anything_goes_with_123@')

# ----------------------------------< Cross Origin Implementation >----------------------------------
CORS(app)

# ----------------------------------< MongoEngine Initialization >-----------------------------------
app.config['MONGODB_SETTINGS'] = [
    {
        'host': environ.get('DATABASE_URL')
    }
]
initialize_database(app)

# ---------------------------------------< Exception Handler >---------------------------------------
@app.errorhandler(ValidationError)
def validation_error_handler(err: ValidationError):
    logger.exception(err)
    return {
            'error': err.message,
            'message': 'MongoEngine Validation Error',
        }, 400

@app.errorhandler(Exception)
def all_error_handler(err):
    logger.exception(err)
    return {'message': 'Unexpected Error Occured'}, 500

# ---------------------------------------< All Routes Import >---------------------------------------
from views import v1_views
app.register_blueprint(v1_views)

# ----------------------------------------< Run Application >----------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9010, debug=True)
