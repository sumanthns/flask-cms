from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security
from flask_wtf import CsrfProtect

db = SQLAlchemy()
security = Security()
csrf = CsrfProtect()
