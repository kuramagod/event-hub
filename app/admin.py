from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from app.auth.services import get_current_user


COMMON_LABELS = {
    "id": "ID",
    "name": "Название",
    "email": "Email",
    "phone": "Телефон",
}


class ProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        user = get_current_user()
        return user is not None and user.role_id == 1

    def inaccessible_callback(self, name, **kwargs):
        user = get_current_user()

        if user is None:
            return redirect(url_for("auth.login"))

        return redirect(url_for("main.index"))


class AdminModelView(ModelView):
    page_size = 20
    can_export = True
    create_modal = True
    edit_modal = True
    can_view_details = True

    def is_accessible(self):
        user = get_current_user()
        return user is not None and user.role_id == 1

    def inaccessible_callback(self, name, **kwargs):
        if get_current_user() is None:
            return redirect(url_for("auth.login"))
        return redirect(url_for("main.index"))


class UserAdminView(AdminModelView):
    column_list = ["id", "fullname", "email", "phone", "role", "events", "favorite"]
    column_labels = {
        **COMMON_LABELS,
        "fullname": "Полное имя",
        "role": "Роль",
        "events": "Мероприятия",
        "favorite": "Избранное",
    }
    column_searchable_list = ["fullname", "email", "phone"]
    column_filters = ["role", "email"]
    form_columns = ["fullname", "email", "phone", "role"]
    column_default_sort = ("id", True)
    can_create = False
    can_delete = False
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash", "events", "favorite"]


class RoleAdminView(AdminModelView):
    column_list = ["id", "name", "user"]
    column_labels = {**COMMON_LABELS, "name": "Название роли", "user": "Пользователи"}
    column_searchable_list = ["name"]
    form_columns = ["name"]
    can_view_details = False


class CategoryAdminView(AdminModelView):
    column_list = ["id", "name", "color", "events"]
    column_labels = {**COMMON_LABELS, "color": "Цвет", "events": "Мероприятия"}
    column_searchable_list = ["name"]
    form_columns = ["name", "color"]


class CityAdminView(AdminModelView):
    column_list = ["id", "name", "events"]
    column_labels = {**COMMON_LABELS, "events": "Мероприятия"}
    column_searchable_list = ["name"]
    form_columns = ["name"]


class EventAdminView(AdminModelView):
    column_list = ["id", "name", "category", "city", "date", "price", "author", "slug"]
    column_labels = {
        **COMMON_LABELS,
        "category": "Категория",
        "city": "Город",
        "date": "Дата",
        "price": "Цена",
        "author": "Автор",
        "slug": "slug",
    }
    column_searchable_list = ["name", "description", "address"]
    column_filters = ["category", "city", "author", "date"]
    form_columns = [
        "name",
        "category",
        "image_url",
        "city",
        "address",
        "date",
        "price",
        "description",
        "author",
        "external_url",
    ]
    form_excluded_columns = ["slug"]
    readonly_fields = ["slug"]
    column_default_sort = ("date", True)


class FavoriteAdminView(AdminModelView):
    column_list = ["id", "user", "event"]
    column_labels = {"user": "Пользователь", "event": "Мероприятие"}
    column_filters = ["user", "event"]
    form_columns = ["user", "event"]
    can_view_details = False