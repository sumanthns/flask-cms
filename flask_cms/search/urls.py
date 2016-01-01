from flask_cms.search import search
from flask_cms.search.views import SearchView

routes = [((search,), ('', SearchView.as_view('search')), )]
