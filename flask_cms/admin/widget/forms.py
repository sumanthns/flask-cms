from flask_wtf import Form
from werkzeug.utils import import_string

from wtforms import StringField, SelectField, FieldList, FormField, TextField, TextAreaField
from wtforms.validators import DataRequired, InputRequired
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
