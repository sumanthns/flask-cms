from flask import render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_cms.admin.member.forms import AdminMemberForm, AdminRoleForm
from flask_cms.admin.views import AdminView
from flask_cms.app.models.roles import Role
from flask_cms.app.models.users import User
from flask_cms.ext import db
from flask_cms.utils import get_object_or_404, flash_errors


class CreateMemberView(AdminView):
    def get(self):
        form = AdminMemberForm()
        return render_template("member/admin_member_form.html", form=form)

    def post(self):
        form = AdminMemberForm()
        if form.validate_on_submit():
            member = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
            )

            for role_id in form.roles.data:
                role = get_object_or_404(Role, Role.id == int(role_id))
                member.roles.append(role)
            db.session.add(member)
            db.session.commit()
            flash("Successfully created member")
            return redirect(url_for('admin.list_member'))

        flash_errors(form)
        return render_template("member/admin_member_form.html", form=form)


class CreateRoleView(AdminView):
    def get(self):
        form = AdminRoleForm()
        return render_template("member/admin_role_form.html", form=form)

    def post(self):
        form = AdminRoleForm()
        if form.validate_on_submit():
            role = Role(name=form.name.data,
                        description=form.description.data, )
            db.session.add(role)
            db.session.commit()
            flash("Successfully created role")
            return redirect(url_for('admin.list_member'))

        flash_errors(form)
        return render_template("member/admin_role_form.html", form=form)


class EditMemberView(AdminView):
    def get(self, member_id):
        member = get_object_or_404(User, User.id == int(member_id))
        form = AdminMemberForm(member)
        return render_template("member/admin_member_form.html", form=form)

    def post(self, member_id):
        member = get_object_or_404(User, User.id == int(member_id))
        form = AdminMemberForm()
        if form.validate_on_submit():
            member.first_name = form.first_name.data
            member.last_name = form.last_name.data
            member.email = form.email.data
            member.roles = []

            for role_id in form.roles.data:
                role = get_object_or_404(Role, Role.id == int(role_id))
                member.roles.append(role)
            db.session.commit()
            flash("Successfully updated member")
        else:
            flash_errors(form)

        return render_template("member/admin_member_form.html", form=form)


class DeleteMemberView(AdminView):
    def get(self, member_id):
        member = get_object_or_404(User, User.id == int(member_id))
        db.session.delete(member)
        db.session.commit()
        flash("Successfully deleted member")
        return redirect(url_for('admin.list_member'))


class DeleteRoleView(AdminView):
    def get(self, role_id):
        role = get_object_or_404(Role, Role.id == int(role_id))
        db.session.delete(role)
        db.session.commit()
        flash("Successfully deleted member")
        return redirect(url_for('admin.list_member'))


class MemberListView(AdminView):
    def get(self):
        members = User.query.all()
        roles = Role.query.all()
        return render_template("member/list_member.html",
                               members=members,
                               roles=roles)
