from flask import redirect, render_template, url_for

from app.auth.services import get_current_user, login_required
from app.db import db_session
from .forms import ProfileForm, ChangePasswordForm
from . import bp


@bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    current_user = get_current_user()
    
    profile_form = ProfileForm(obj=current_user, user=current_user)
    change_password_form = ChangePasswordForm(user=current_user)
   
    if profile_form.submit_profile.data and profile_form.validate():
        current_user.fullname = profile_form.fullname.data
        current_user.phone = profile_form.phone.data
        
        db_session.commit()
        return redirect(url_for("profile.profile"))
    
    if change_password_form.submit_password.data and change_password_form.validate():
        current_user.set_password(change_password_form.new_password.data)
        
        db_session.commit()
        return redirect(url_for("profile.profile"))


    return render_template("profile/profile.html", profile_form=profile_form, change_password_form=change_password_form)
