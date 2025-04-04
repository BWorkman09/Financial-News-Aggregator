from flask import Flask
from flask_cors import CORS
from flasgger import Swagger # Only required if you want to use Swagger UI
import yaml
from api.routes import api_bp
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


# Using Blueprints to organize routes in a Flask application
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
# We are using Blueprints to organize our routes in our Flask application.  This
#  allows us to separate the routes into different files, which can help keep our
#  code organized and easier to maintain.  In this case, we have a single blueprint
#  that is defined in the api/routes.py file.  We import that blueprint here and
#  register it with our Flask application.  The blueprint is registered with a
#  prefix of "/api", which means that all routes defined in the blueprint will
#  be prefixed with "/api".  For example, a route defined in the blueprint as
#  "/users" will be accessible at "/api/users" in the application.


def create_app():
   app = Flask(__name__)
   CORS(app)

   # Database setup
   DATABASE_PATH = Path(__file__).parent / "data" / "News_Aggregator.db"
   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

   # Initialize SQLAlchemy with the app
   db.init_app(app)

   # Import models (after db initialization)
   from api.models import User, Article, Category, UserPreference

   # Import and register blueprint
   from api.routes import api_bp
   app.register_blueprint(api_bp, url_prefix='/api')

   # Create tables
   with app.app_context():
       db.create_all()
       
   return app

if __name__ == '__main__':
   app = create_app()
   app.run(debug=True)
   
