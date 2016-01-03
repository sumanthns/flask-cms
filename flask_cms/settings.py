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
        'flask_cms.search.urls.routes',
    ]

    BLUEPRINTS = [
        'flask_cms.core.core',
        'flask_cms.member.member',
        'flask_cms.page.page',
        'flask_cms.admin.admin',
        'flask_cms.widget.widget',
        'flask_cms.search.search',
    ]

    EXTENSIONS = [
        'db',
        'csrf',
        'mail',
    ]

    CONTEXT_PROCESSORS = [
        'flask_cms.page.context_processors.create_breadcrumbs_snippet',
        'flask_cms.page.context_processors.add_grouper',
        'flask_cms.page.context_processors.add_navbar',
        'flask_cms.page.context_processors.add_flash_form_errors',
        'flask_cms.search.context_processors.add_search_form',
        'flask_cms.core.context_processors.add_registerable',
        'flask_cms.core.context_processors.add_recoverable',
        'flask_cms.core.context_processors.add_confirmable',
    ]

    # supported widgets that admin can create
    WIDGET_CREATE_FORMS = [
        ('poll', 'flask_cms.admin.widget.forms.PollForm'),
        ('carousel', 'flask_cms.admin.widget.forms.CarouselForm'),
        ('split_panel', 'flask_cms.admin.widget.forms.SplitPanelForm'),
        ('map', 'flask_cms.admin.widget.forms.MapForm'),
        ('grid', 'flask_cms.admin.widget.forms.GridForm'),
    ]

    # supported widget models
    WIDGET_MODELS = [
        ('poll', 'flask_cms.widget.models.poll.Poll'),
        ('carousel', 'flask_cms.widget.models.carousel.Carousel'),
        ('split_panel', 'flask_cms.widget.models.split_panel.SplitPanel'),
        ('map', 'flask_cms.widget.models.map.Map'),
        ('grid', 'flask_cms.widget.models.grid.Grid'),
    ]

    # available grid types
    GRID_TYPES = [
        '1_by_3_grid',
    ]

    # search [model, (searchable_columns), (columns_to_select)]
    SEARCHABLE_MODELS = [
        ['flask_cms.page.models.Page',
         ('title', 'description', 'content'),
         ('title', 'description', 'slug'), ],
        ['flask_cms.app.models.users.User',
         ('first_name', 'last_name', 'email'),
         ('first_name', 'last_name', "email", "id"), ],
    ]

    # security configs
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "secret_password_salt"
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = True

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True
    SECURITY_RECOVERABLE = False
    SECURITY_REGISTERABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_CONFIRMABLE = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/flaskcms'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    HOSTNAME = os.environ.get("HOSTNAME")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
