import os
import yaml
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def load_config(app, config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
        app.config.update(config_data)

def create_app():
    app = Flask(__name__)

    config_path = os.getenv('CONFIG_PATH', 'config/development.yaml')
    load_config(app, config_path)

    mongo.init_app(app)

    from .routes.project_routes import project_blueprint
    app.register_blueprint(project_blueprint)
    
    from .routes.task_routes import task_blueprint
    app.register_blueprint(task_blueprint)
    
    from .routes.team_routes import team_blueprint
    app.register_blueprint(team_blueprint)
    
    from .routes.comment_routes import comment_blueprint
    app.register_blueprint(comment_blueprint)

    return app
