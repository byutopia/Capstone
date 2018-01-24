from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

wago_mod = Blueprint('wago', __name__)
wago_hit = False

# set route
@wago_mod.route('/wago', methods = ['GET', 'POST'])
def wago():
    global wago_hit

    if request.method == 'POST':
        wago_hit = True
        return 'ok'
    else:
        return render_template("wago.html", data={'status': wago_hit})
