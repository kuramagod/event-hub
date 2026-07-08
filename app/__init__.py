import os

from flask import Flask 


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.template_folder = "templates"
    app.static_folder = "static"

    from . import db
    db.init_app(app)

    from .auth import bp as auth_bp
    from .event import bp as event_bp
    from .main import bp as main_bp
    from .profile import bp as profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)

    @app.context_processor
    def inject_user():
        from app.auth import get_current_user
        return dict(user=get_current_user())

    return app
