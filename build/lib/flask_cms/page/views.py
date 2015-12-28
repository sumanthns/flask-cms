from flask import render_template
from flask.views import MethodView
from werkzeug.exceptions import abort

from flask_cms.page.models import Page
from flask.ext.security import current_user
from flask_cms.utils import get_object_or_404


class PageView(MethodView):
    def get(self, slug):
        page = get_object_or_404(Page, Page.slug == slug)

        if page.login_required:
            if not current_user.is_authenticated:
                abort(404)

        if not page.publish:
            abort(404)

        return render_template('page.html', page=page)
