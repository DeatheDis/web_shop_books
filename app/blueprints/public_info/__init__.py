from flask import Blueprint

public_info_blueprint = Blueprint('public_info', __name__, url_prefix='')

from . import routes
