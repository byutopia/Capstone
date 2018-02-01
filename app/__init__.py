from flask import Flask, Response, render_template, send_from_directory
from flask_socketio import SocketIO
import json


socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.debug = debug
    app.config["SECRET_KEY"] = 'strong secret'

    from modules.rainmachine.controller import rainmachine_mod as rainmachine_module
    from modules.purpleair.controller import purpleair_mod as purpleair_module
    from modules.wago.controller import wago_mod as wago_module
    from modules.camera.controller import camera_mod as camera_module

    app.register_blueprint(rainmachine_module)
    app.register_blueprint(purpleair_module)
    app.register_blueprint(wago_module)
    app.register_blueprint(camera_module)

    import jinja2.exceptions
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/<pagename>')
    def admin(pagename):
        return render_template(pagename+'.html')

    @app.route('/<path:resource>')
    def serve_static_resource(resource):
        return send_from_directory(app.static_folder, resource)

    @app.route('/teapot')
    def teapot():
        return Response(json.dumps({'message': 'I am a teapot!'}), status=418, mimetype='application/json')

    @app.errorhandler(jinja2.exceptions.TemplateNotFound)
    def template_not_found(e):
        return not_found(e)

    @app.errorhandler(404)
    def not_found(e):
        return '<strong>Page Not Found!</strong>', 404

    socketio.init_app(app)
    return app
