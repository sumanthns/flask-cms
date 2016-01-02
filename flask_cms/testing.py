import unittest
from flask_cms.admin.template.models import Template

from app import app
from app.models.roles import Role
from ext import db
from app.models.users import User
from flask.ext.security.utils import verify_password
from page.models import Page


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.admin_role = self._create_admin_role()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_user(self, user):
        self.app.post("/login",
                      data={'email': user.email,
                            'password': user.password})

    def _create_user(self, email, password, active):
        user = User(email=email, password=password, active=active)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            return User.query.filter_by(
                email=user.email).first()

    def _create_admin_role(self):
        admin_role = Role(name='admin', description='fu')
        db.session.add(admin_role)
        db.session.commit()
        return admin_role

    def _create_admin_user(self, email, password, active):
        user = User(email=email, password=password, active=active)
        user.roles = [self.admin_role]

        with app.app_context():
            db.session.add(user)
            db.session.commit()

            return User.query.filter_by(
                email=user.email).first()

    def _get_user(self, **kwargs):
        user = User.query.\
            filter_by(**kwargs).first()
        return user

    def _get_page(self, **kwargs):
        page = Page.query.\
            filter_by(**kwargs).first()
        return page

    def _get_template(self, **kwargs):
        template = Template.query.\
            filter_by(**kwargs).first()
        return template

    def _create_page(self, **kwargs):
        page = Page(**kwargs)
        db.session.add(page)
        db.session.commit()
        return page

    def _create_template(self, **kwargs):
        template = Template(**kwargs)
        db.session.add(template)
        db.session.commit()
        return template

    def _create_model(self, model, **kwargs):
        model = model(**kwargs)
        db.session.add(model)
        db.session.commit()
        return model

    def _delete_model(self, model):
        db.session.delete(model)
        db.session.commit()

    def _get_model(self, model, **kwargs):
        model = model.query.filter_by(**kwargs).first()
        return model

    def _verify_password(self, expect_password, password):
        with app.app_context():
            return verify_password(expect_password, password)

if __name__ == '__main__':
    unittest.main()
