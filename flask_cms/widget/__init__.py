from flask import Blueprint

widget = Blueprint("widget", __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/widget')
