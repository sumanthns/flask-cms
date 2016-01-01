from flask import Blueprint

search = Blueprint("search", __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/search')
