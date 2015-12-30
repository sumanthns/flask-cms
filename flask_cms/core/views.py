from flask import render_template, url_for
from flask.views import MethodView
from werkzeug.utils import redirect

from flask_cms.page.models import Page


class IndexView(MethodView):
    def get(self):
        home_page = Page.query.filter_by(slug='home').first
        if home_page is not None:
            return redirect(url_for('page.show', slug='home'))

        index_page = Page.query.filter_by(slug='index').first
        if index_page is not None:
            return redirect(url_for('page.show', slug='index'))

        return render_template('index.html')
