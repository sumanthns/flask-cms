from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class TemplateForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])

    def __init__(self, template=None):
        Form.__init__(self)
        if template is not None:
            self.name.data = template.name
            self.description.data = template.description
