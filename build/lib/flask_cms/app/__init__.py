import os
from flask_cms.factory import AppFactory

from flask_cms.settings import DevelopmentConfig, \
    TestConfig, ProductionConfig


configs = {'development': DevelopmentConfig,
           'test': TestConfig,
           'prod': ProductionConfig,
           }

config = configs[os.environ.get("ENV", "development")]
app = AppFactory(config=config, name=__name__).get_app()
