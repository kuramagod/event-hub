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

    from . import auth, event, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(event.bp)
    app.register_blueprint(main.bp)

    @app.context_processor
    def inject_user():
        from app.auth import get_current_user
        return dict(user=get_current_user())

    return app
