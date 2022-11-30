from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_database(app):
    db.init_app(app)
