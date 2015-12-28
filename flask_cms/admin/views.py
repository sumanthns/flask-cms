from flask import render_template
from flask.views import MethodView

from flask.ext.security import roles_accepted, \
    login_required
from flask_cms.admin.template.models import Template
from flask_cms.page.models import Page


class AdminView(MethodView):
    decorators = [login_required,
                  roles_accepted('admin')]


class IndexView(AdminView):
    def get(self):
        root_pages = Page.query.filter_by(level=0). \
            order_by(Page.created_at.desc()).all()

        templates = Template.query.all()
        return render_template("admin_index.html",
                               pages=root_pages,
                               templates=templates)
