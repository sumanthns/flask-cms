import os
from flask import render_template

from flask_cms.factory import AppFactory
from flask_cms.settings import DevelopmentConfig, \
    TestConfig, ProductionConfig


configs = {'development': DevelopmentConfig,
           'test': TestConfig,
           'prod': ProductionConfig,
           }

config = configs[os.environ.get("ENV", "development")]
app = AppFactory(config=config, name=__name__).get_app()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
