from flask import Blueprint

main_blueprint = Blueprint('index', __name__, url_prefix='')

from . import routes
