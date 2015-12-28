from flask_cms.core import core
from .views import IndexView

routes = [((core,), ('', IndexView.as_view('index')), )]
