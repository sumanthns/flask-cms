from flask import render_template, url_for, flash, request
from flask.views import MethodView
from flask.ext.security import current_user, \
    login_required
from flask.ext.security.utils import encrypt_password
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask_cms.app.models.users import User
from flask_cms.ext import db
from flask_cms.member.forms import MemberForm, ChangePasswordForm
from flask_cms.utils import get_object_or_404


class MemberView(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.query.filter_by(
            id=current_user.id).first()
        form = MemberForm(user)
        return render_template('member.html', form=form)

    def post(self):
        user = User.query.filter_by(
            id=current_user.id).first()
        form = MemberForm()
        print request.form
        if form.validate_on_submit():
            print request.form
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            form.user = user
            db.session.commit()
            flash("Profile updated successfully")
            return redirect(
                url_for('member.show'))
        return render_template('member.html', form=form)


class OtherMemberView(MethodView):
    decorators = [login_required]

    def get(self, member_id):
        if current_user.id == int(member_id):
            form = MemberForm(current_user)
            return render_template('member.html', form=form)

        user = get_object_or_404(User, User.id == member_id)
        return render_template("other_member.html", user=user)


class ChangePasswordView(MethodView):
    decorators = [login_required]

    def get(self):
        form = ChangePasswordForm()
        return render_template("change_password.html",
                               form=form)

    def post(self):
        form = ChangePasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(
                email=current_user.email).first()
            user.password = encrypt_password(
                form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password updated successfully")
            return redirect(url_for("member.show"))
        return render_template("change_password.html",
                               form=form)
