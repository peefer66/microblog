from flask import render_template
from app import app, db

'''
Flask provides a mechanism for an application to install its own errors
page using custom error handler @errorhandler
'''
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollack()
    return render_template('500.html'), 500
