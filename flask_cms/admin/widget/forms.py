from flask import flash
from flask_wtf import Form
from werkzeug.utils import import_string
from wtforms import StringField, SelectField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired

from flask_cms.page.models import Page
from flask_cms.utils import CKTextAreaField
from flask_cms.widget.models.widget_type import WidgetType


class WidgetForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    types = SelectField('types', validators=[DataRequired()])

    def __init__(self):
        Form.__init__(self)
        self.types.choices = [(t.id, t.name) for t in WidgetType.query.all()]
        self.types.choices.insert(0, (0, ''))
        self.types.coerce = int


class PollForm(WidgetForm):
    question = StringField('Question', validators=[DataRequired()])
    choice1 = StringField('Choice 1')
    choice2 = StringField('Choice 2')
    choice3 = StringField('Choice 3')
    choice4 = StringField('Choice 4')

    def __init__(self):
        WidgetForm.__init__(self)
        self.types.data = WidgetType.query.filter_by(name='poll').first().id


class CarouselImageForm(Form):
    image_link = StringField('Image Link')
    image_caption = StringField('Caption')
    image_description = StringField('Description')


class CarouselForm(WidgetForm):
    images = FieldList(FormField(CarouselImageForm), min_entries=1)

    def __init__(self):
        WidgetForm.__init__(self)
        self.types.data = WidgetType.query.filter_by(name='carousel').first().id


class GridPageForm(Form):
    page_slug = StringField('Page Slug', validators=[DataRequired()])


class GridForm(WidgetForm):
    grid_pages = FieldList(FormField(GridPageForm), min_entries=1)
    grid_types = SelectField('grid_type', validators=[DataRequired()])

    def __init__(self):
        from flask_cms.app import app
        WidgetForm.__init__(self)
        self.types.data = WidgetType.query.filter_by(name='grid').first().id
        self.grid_types.choices = [(t, t) for t in app.config['GRID_TYPES']]

    def validate(self):
        if not WidgetForm.validate(self):
            return False

        for page in self.grid_pages:
            page_exists = Page.query.filter_by(slug=page.page_slug.data).first()
            if page_exists is None:
                flash("Page {} does not exist".format(page.page_slug.data), "error")
                return False

        return True


class SplitPanelForm(WidgetForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    multimedia_types = SelectField('Type', choices=[("image", "image"), ("video", "video"), ("audio", "audio")],
                                   validators=[DataRequired()])
    align = SelectField('Align', choices=[("right", "right"), ("left", "left")], validators=[DataRequired()])
    size = SelectField('size', choices=[("100%", "100%"), ("75%", "75%"), ("50%", "50%"), ("25%", "25%")],
                       validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])

    def __init__(self):
        WidgetForm.__init__(self)
        self.types.data = WidgetType.query.filter_by(name='split_panel').first().id


class MapForm(WidgetForm):
    title = StringField('Title', validators=[DataRequired()])
    address = CKTextAreaField('Content', validators=[DataRequired()])
    longitude = StringField('Title', validators=[DataRequired()])
    latitude = StringField('Title', validators=[DataRequired()])

    def __init__(self):
        WidgetForm.__init__(self)
        self.types.data = WidgetType.query.filter_by(name='map').first().id


class WidgetNotSupportedException(Exception):
    pass


class WidgetFormFactory(object):
    def __init__(self, type=None):
        self.type = type

    def get_widget_form(self):
        if self.type is None:
            return WidgetForm()
        from flask_cms.app import app

        for wf in app.config.get("WIDGET_CREATE_FORMS", []):
            widget, form = wf
            if self.type == widget:
                form = import_string(form)
                return form()

        raise WidgetNotSupportedException()
