import flask
import settings
from bha import bp as bha_bp


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(settings)

    settings.db.init_app(app)
    settings.bootstrap.init_app(app)

    app.register_blueprint(bha_bp)

    return app
