from flask import request, url_for, flash
from flask.views import MethodView
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

from flask_cms.ext import db
from flask_cms.page.models import Page
from flask.ext.security import current_user
from flask_cms.utils import get_object_or_404
from flask_cms.widget.models.poll import Choice


class PollVoteView(MethodView):
    def post(self, slug, widget_id):
        print request.form
        page = get_object_or_404(Page, Page.slug == slug)
        if page.login_required:
            if not current_user.is_authenticated:
                abort(404)

        choice = request.form.get('choice', None)
        if not choice:
            flash("Choice is not valid", "error")
            return redirect(url_for('page.show', slug=page.slug))
        poll_choice = get_object_or_404(Choice, Choice.id == int(choice))
        poll_choice.vote += 1
        db.session.commit()
        flash("Thank you for voting")
        return redirect(url_for('page.show', slug=page.slug))
