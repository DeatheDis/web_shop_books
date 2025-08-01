from flask import Blueprint

book_blueprint = Blueprint('book', __name__, url_prefix='')

from . import routes
