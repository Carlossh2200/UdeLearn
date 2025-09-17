from flask import Flask, request
from flask_cors import CORS
from config import config

#Routes
from routes import Collections
app = Flask(__name__)
CORS(app,resources={"*" : {"origins": "http://localhost:5173"}})

def page_not_found(error):
    return "<h1>Page not found</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])

    #Blueprints
    app.register_blueprint(Collections.main,url_prefix='/api/collections')

    #Error handlers
    app.register_error_handler(404,page_not_found)
    app.run()