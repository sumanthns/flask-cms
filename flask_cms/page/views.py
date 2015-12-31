from flask import render_template, flash, url_for
from flask.views import MethodView
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from flask_cms.page.models import Page
from flask.ext.security import current_user
from flask_cms.utils import get_object_or_404


class PageView(MethodView):
    def get(self, slug):
        page = get_object_or_404(Page, Page.slug == slug)

        if page.login_required:
            if not current_user.is_authenticated:
                flash("Please login to view this page", "error")
                return redirect(url_for('core.index'))

        if not page.publish:
            abort(404)

        return render_template('base_page.html', page=page)
