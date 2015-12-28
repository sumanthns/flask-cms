from flask import Flask
from werkzeug.utils import import_string
from flask.ext.security import SQLAlchemyUserDatastore
from flask_cms.ext import db, security


class NoBlueprintException(Exception):
    pass


class NoRouteModuleException(Exception):
    pass


class NoExtensionException(Exception):
    pass


class NoContextProcessorException(Exception):
    pass


def _get_imported_stuff_by_path(path):
    module_name, object_name = path.rsplit('.', 1)
    module = import_string(module_name)

    return module, object_name


class AppFactory(object):
    def __init__(self, config, name):
        self.app = None
        self.config = config
        self.name = name

    def _build_app(self):
        self.app = Flask(self.name)
        self._add_config()
        self._bind_extensions()
        self._register_blueprints()
        self._register_routes()
        self._register_context_processors()
        self._bind_security()

    def _add_config(self):
        self.app.config.from_object(self.config)

    def _bind_extensions(self):
        for ext_path in self.app.config.get('EXTENSIONS', []):
            module, e_name = _get_imported_stuff_by_path('flask_cms.ext.{}'.format(ext_path))
            if not hasattr(module, e_name):
                raise NoExtensionException('No {e_name} extension found'.format(e_name=e_name))
            ext = getattr(module, e_name)
            if getattr(ext, 'init_app', False):
                ext.init_app(self.app)
            else:
                ext(self.app)

    def get_app(self):
        self._build_app()
        return self.app

    def _register_blueprints(self):
        self._bp = {}
        for blueprint_path in self.app.config.get('BLUEPRINTS', []):
            module, b_name = \
                _get_imported_stuff_by_path(blueprint_path)
            if hasattr(module, b_name):
                self.app.register_blueprint(getattr(module, b_name))
            else:
                raise NoBlueprintException(
                    'No {bp_name} blueprint found'.format(bp_name=b_name))

    def _register_routes(self):
        for url_module in self.app.config.get('URL_MODULES', []):
            module, r_name = _get_imported_stuff_by_path(url_module)
            if hasattr(module, r_name):
                self._setup_routes(getattr(module, r_name))
            else:
                raise NoRouteModuleException('No {r_name} url module found'.format(r_name=r_name))

    def _setup_routes(self, routes):
        for route in routes:
            blueprint, rules = route[0], route[1:]
            for pattern, view in rules:
                if isinstance(blueprint, tuple):
                    blueprint = blueprint[0]
                blueprint.add_url_rule(pattern, view_func=view)
            if blueprint not in self.app.blueprints:
                self.app.register_blueprint(blueprint)

    def _register_context_processors(self):
        for processor_path in self.app.config.get('CONTEXT_PROCESSORS', []):
            module, p_name = _get_imported_stuff_by_path(processor_path)
            if hasattr(module, p_name):
                self.app.context_processor(getattr(module, p_name))
            else:
                raise NoContextProcessorException('No {cp_name} context processor found'.format(cp_name=p_name))

    def _bind_security(self):
        from flask_cms.app.models.users import User
        from flask_cms.app.models.roles import Role

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(self.app, user_datastore)
