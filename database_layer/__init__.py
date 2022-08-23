from flask_mongoengine import MongoEngine

mongodb = MongoEngine()

def initialize_database(app):
    mongodb.init_app(app)
    