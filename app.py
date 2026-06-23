from flask import Flask
from flask_login import LoginManager
from config import config
from models import db, bcrypt, User


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para continuar.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.catalog import catalog_bp
    from routes.player import player_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(catalog_bp)
    app.register_blueprint(player_bp)

    # Create tables on first run
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='127.0.0.1', port=5000)
