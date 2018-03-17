#!/usr/bin/env python

#from flask import Flask, url_for, render_template, send_from_directory
#from flask_socketio import SocketIO, emit
#import jinja2.exceptions
#from rainmachine.controller import rainmachine_mod as rainmachine_module
#from purpleair.controller import purpleair_mod as purpleair_module
#from wago.controller import wago_mod as wago_module
from app import create_app, socketio

app = create_app(debug=True)
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'strong secret'
#socketio = SocketIO(app)

#@app.route('/')
#def index():
#    return render_template('index.html')

# Register blueprint
# app.register_blueprint(module name)

#rainmachine
#app.register_blueprint(rainmachine_module)
#app.register_blueprint(purpleair_module)
#app.register_blueprint(wago_module)

#@app.route('/<pagename>')
#def admin(pagename):
#    return render_template(pagename+'.html')

#@app.route('/<path:resource>')
#def serve_static_resource(resource):
#    return send_from_directory('static/', resource)

#@app.errorhandler(jinja2.exceptions.TemplateNotFound)
#def template_not_found(e):
#    return not_found(e)

#@app.errorhandler(404)
#def not_found(e):
#    return '<strong>Page Not Found!</strong>', 404

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, log_output=True)
