from flask import Blueprint

from .template import models


admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  url_prefix='/admin'
                  )
