import os

from flask import Flask
from flask_admin import Admin


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.template_folder = "templates"
    app.static_folder = "static"

    from .admin import ProtectedAdminIndexView, AdminModelView
    admin = Admin(app, name='Admin panel', index_view=ProtectedAdminIndexView())

    from . import db, models
    db.init_app(app)
    
    admin.add_view(AdminModelView(models.User, db.db_session, category="User"))
    admin.add_view(AdminModelView(models.Role, db.db_session, category="User"))
    admin.add_view(AdminModelView(models.Favorite, db.db_session, category="User"))
    admin.add_view(AdminModelView(models.Event, db.db_session, category="Event", endpoint="admin_event"))
    admin.add_view(AdminModelView(models.Category, db.db_session, category="Event"))
    admin.add_view(AdminModelView(models.City, db.db_session, category="Event"))

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
