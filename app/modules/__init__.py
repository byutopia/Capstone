from flask import Flask
import jinja2.exceptions
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = 'strong secret'

    from default.controller import default_mod as default_module
    from rainmachine.controller import rainmachine_mod as rainmachine_module
    from purpleair.controller import purpleair_mod as purpleair_module
    from wago.controller import wago_mod as wago_module

    app.register_blueprint(default_module)
    app.register_blueprint(rainmachine_module)
    app.register_blueprint(purpleair_module)
    app.register_blueprint(wago_module)

    socketio.init_app(app)
    return app
