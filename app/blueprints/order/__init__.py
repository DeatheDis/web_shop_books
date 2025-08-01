from flask import Blueprint

order_blueprint = Blueprint('order', __name__, url_prefix='')
from . import routes

