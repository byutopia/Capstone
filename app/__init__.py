from flask import Flask
#create the app
app = Flask(__name__)

#import modules from folder.filename
from home.controller import home_mod as home_module

# Register blueprint
app.register_blueprint(home_module)
# app.register_blueprint(module name)

