from flask import flash
from flask_wtf import Form
from wtforms import StringField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired
from flask_cms.admin.template.models import Template
from flask_cms.page.models import Page

from flask_cms.utils import CKTextAreaField
from flask_cms.widget.models.widget import Widget


class EditPage(Form):
    slug = StringField('Slug', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    templates = SelectField('templates', validators=[DataRequired()])
    header_image = StringField('Header Image')
    content = CKTextAreaField('Content')
    login_required = BooleanField("login_required", default=False)
    show_in_nav = BooleanField("show_in_nav", default=False)
    parent_slug = HiddenField("parent_slug")

    def __init__(self, page=None):
        Form.__init__(self)
        self.page = page
        self.templates.choices = [(t.id, t.name) for t in Template.query.all()]
        self.templates.coerce = int
        if self.page:
            self.slug.data = page.slug
            self.title.data = page.title
            self.description.data = page.description
            self.content.data = page.content
            self.login_required.data = page.login_required
            self.show_in_nav.data = page.show_in_nav
            self.templates.data = page.template_id
            self.header_image.data = page.header_image

    def validate(self):
        if not Form.validate(self):
            return False

        if self.page is None:
            existing_page = Page.query.filter_by(
                slug=self.slug.data).first()

            if existing_page is not None:
                flash("Page with same slug already exists.", "error")
                return False

        return True


class AddWidgetToPageForm(Form):
    widgets = SelectField('widgets', coerce=int)

    def __init__(self):
        Form.__init__(self)
        self.widgets.choices = [(w.id, w.name) for w in Widget.query.all()]
