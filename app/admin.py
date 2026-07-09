from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from app.auth.services import get_current_user


class ProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        user = get_current_user()
        return user is not None and user.role_id == 1
    
    def inaccessible_callback(self, name, **kwargs):
        if get_current_user() is None:
            return redirect(url_for("auth.login"))
        return redirect(url_for("main.index"))


class AdminModelView(ModelView):
    def is_accessible(self):
        user = get_current_user()
        return user is not None and user.role_id == 1
    
    def inaccessible_callback(self, name, **kwargs):
        if get_current_user() is None:
            return redirect(url_for("auth.login"))
        return redirect(url_for("main.index"))