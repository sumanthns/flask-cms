from flask import render_template, url_for, request, flash
from werkzeug.utils import redirect

from flask_cms.admin.page.forms import EditPage
from flask_cms.admin.views import AdminView
from flask_cms.ext import db
from flask_cms.page.models import Page
from flask_cms.utils import get_object_or_404


class EditPageView(AdminView):
    def get(self, slug):
        page = get_object_or_404(Page, Page.slug == slug)
        form = EditPage(page)
        return render_template('page/admin_page.html', form=form)

    def post(self, slug):
        page = get_object_or_404(Page, Page.slug == slug)
        form = EditPage(page)
        if form.validate_on_submit():
            page.slug = request.form.get('slug')
            page.title = request.form.get('title')
            page.description = request.form.get('description')
            page.content = request.form.get('content')
            page.login_required = 'login_required' in request.form
            page.show_in_nav = 'show_in_nav' in request.form
            page.publish = 'publish' in request.form

            db.session.commit()
            return redirect(url_for('admin.edit_page', slug=page.slug))
        return render_template('page/admin_page.html', form=form)


class AddPageView(AdminView):
    def get(self):
        form = EditPage()
        if request.args.get('parent'):
            parent = Page.query.filter_by(
                slug=request.args.get("parent")).first()
            if parent:
                form.parent_slug.data = parent.slug

        return render_template('page/admin_page.html', form=form)

    def post(self):
        form = EditPage()
        if form.validate_on_submit():
            page = Page(
                slug=form.slug.data,
                title=form.title.data,
                description=form.description.data,
                content=form.content.data,
                login_required=form.login_required.data,
                show_in_nav=form.show_in_nav.data,
                publish=form.publish.data,
            )
            page.level = 0

            if request.form.get('parent_slug', None):
                parent = get_object_or_404(
                    Page, Page.slug ==
                    request.form.get('parent_slug'))
                page.parent_id = parent.id
                page.level = parent.level + 1
            db.session.add(page)
            db.session.commit()
            return redirect(url_for('admin.edit_page', slug=page.slug))

        return render_template('page/admin_page.html', form=form)


class DeletePageView(AdminView):
    def get(self, slug):
        page = get_object_or_404(Page, Page.slug == slug)
        db.session.delete(page)
        db.session.commit()
        flash("Successfully deleted page - {}".format(page.slug))
        return redirect(url_for('admin.index'))
