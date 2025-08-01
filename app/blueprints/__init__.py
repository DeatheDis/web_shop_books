from .authentication import auth_blueprint
from .books import book_blueprint
from .cart import cart_blueprint
from .index import main_blueprint
from .order import order_blueprint
from .public_info import public_info_blueprint


def register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(book_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(public_info_blueprint)
