import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DATABASE_QUERY_TIMEOUT = 0.5
    WTF_CSRF_ENABLED = True
    SECRET_KEY = str(uuid.uuid4())
    HOSTNAME = 'localhost'
    DEBUG = True

    URL_MODULES = [
        'flask_cms.core.urls.routes',
        'flask_cms.member.urls.routes',
        'flask_cms.page.urls.routes',
        'flask_cms.admin.urls.routes',
        'flask_cms.widget.urls.routes',
    ]

    BLUEPRINTS = [
        'flask_cms.core.core',
        'flask_cms.member.member',
        'flask_cms.page.page',
        'flask_cms.admin.admin',
        'flask_cms.widget.widget',
    ]

    EXTENSIONS = [
        'db',
    ]

    CONTEXT_PROCESSORS = [
        'flask_cms.page.context_processors.create_breadcrumbs_snippet',
        'flask_cms.page.context_processors.add_grouper',
    ]

    # supported widgets that admin can create
    WIDGET_CREATE_FORMS = [
        ('poll', 'flask_cms.admin.widget.forms.PollForm')
    ]

    # supported widget models
    WIDGET_MODELS = [
        ('poll', 'flask_cms.widget.models.poll.Poll')
    ]

    # security configs
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "secret_password_salt"
    SECURITY_RECOVERABLE = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flaskcms'
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    HOSTNAME = os.environ.get("HOSTNAME")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
