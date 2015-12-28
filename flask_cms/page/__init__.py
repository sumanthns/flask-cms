from flask import Blueprint

page = Blueprint("page", __name__,
                 template_folder='templates',
                 static_folder='static',
                 url_prefix='/page')
