from flask import Flask
#create the app
app = Flask(__name__)

#import modules from folder.filename
from home.controller import home_mod as home_module
from rainmachine.controller import rainmachine_mod as rainmachine_module

# Register blueprint
app.register_blueprint(home_module)
# app.register_blueprint(module name)

#rainmachine
app.register_blueprint(rainmachine_module)
