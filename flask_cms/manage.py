from flask.ext.script import Command, Server, \
    Manager, prompt, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security.utils import encrypt_password
import datetime
from flask_cms.app import app
from flask_cms.ext import db
from flask_cms.app.models import *
from flask_cms.page import models
from flask_cms.admin.template import models
from flask_cms.widget.models import *
from flask_cms.app.models.roles import Role
from flask_cms.app.models.users import User


class DropDbCommand(Command):
    def run(self):
        if prompt_bool('Are you sure to drop database?'):
            print ("Dropping db")
            db.drop_all()


class SetUpCommand(Command):
    def run(self):
        print "creating admin role"
        self.admin_role = self._create_role("admin", "Admin role")
        print "creating member role"
        self.member_role = self._create_role("member", "Member role")
        print "creating admin user"
        self._create_user("admin_user")
        print "creating member user"
        self._create_user("member_user")
        print "Done"

    def _create_role(self, role, description):
        role = Role(name=role, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    def _create_user(self, name):
        if name == "admin_user":
            default_admin_email = "admin@test.com"
            email = prompt("Admin email(default: %s):" % default_admin_email,
                           default=default_admin_email)
            password, confirm_password = self._prompt_password()
            role = self.admin_role
        else:
            email = prompt("Email:", default="member@test.com")
            password, confirm_password = self._prompt_password()
            role = self.member_role

        password = encrypt_password(password)
        user = User(email=email, password=password, active=True, roles=[role],
                    confirmed_at=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()

    def _prompt_password(self):
        default_password = "password"
        password = prompt("Password(default: %s):" % default_password,
                          default=default_password)
        confirm_password = prompt("Confirm Password:", default="password")
        if not password == confirm_password:
            print "Sorry, passwords did not match. Try again"
            self._prompt_password()
        return password, confirm_password


migrate = Migrate(app, db, directory='flask_cms/migrations')
manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)
manager.add_command("setup", SetUpCommand)
manager.add_command("dropdb", DropDbCommand)

if __name__ == "__main__":
    manager.run()
