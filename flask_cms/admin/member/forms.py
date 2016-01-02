from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

from flask_cms.app.models.roles import Role
from flask_cms.utils import MultiCheckboxField


class AdminMemberForm(Form):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    roles = MultiCheckboxField("roles", coerce=int)

    def __init__(self, member=None):
        Form.__init__(self)
        self.roles.choices = [(role.id, role.name) for role in Role.query.all()]
        self.member = member
        if self.member:
            self.first_name.data = self.member.first_name
            self.last_name.data = self.member.last_name
            self.email.data = self.member.email
            self.roles.data = [role.id for role in self.member.roles]


class AdminRoleForm(Form):
    name = StringField("Role Name", validators=[DataRequired()])
    description = StringField("Role Description", validators=[DataRequired()])
