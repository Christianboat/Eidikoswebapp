from flask import Flask
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    from app.admin_routes import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.utils import get_video_embed_url
    app.jinja_env.filters['youtube_embed'] = get_video_embed_url

    return app
