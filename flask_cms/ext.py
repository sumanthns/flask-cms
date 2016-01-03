from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security
from flask_wtf import CsrfProtect
from flask_mail import Mail

db = SQLAlchemy()
security = Security()
csrf = CsrfProtect()
mail = Mail()
