from flask.ext.security import UserMixin
import md5
from flask_cms.ext import db
from flask_cms.app.models.role_user import RoleUser


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), unique=True)
    last_name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=RoleUser.__tablename__,
                            backref=db.backref('users', lazy='dynamic'))

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5.new(self.email.encode('utf-8')).hexdigest(), size)
