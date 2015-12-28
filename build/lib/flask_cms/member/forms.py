from flask import flash
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class MemberForm(Form):
    first_name = StringField('First Name',
                             validators=[DataRequired()])
    last_name = StringField('Last Name',
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired()])

    def __init__(self, user=None):
        Form.__init__(self)
        if user:
            self.user = user
            self.first_name.data = self.user.first_name
            self.last_name.data = self.user.last_name
            self.email.data = self.user.email


class ChangePasswordForm(Form):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        if not self.password.data == self.confirm_password.data:
            flash("Passwords don't match", "error")
            return False

        return True
