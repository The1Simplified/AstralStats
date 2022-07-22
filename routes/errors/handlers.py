import json
from flask import Blueprint, flash, redirect, render_template, url_for
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(400)
def error_400(error):
    """ Page loaded when 400 error occurs """
    return render_template('errors/400.html'), 400


@errors.app_errorhandler(401)
def error_401(error):
    """ Page loaded when 401 error occurs """
    return render_template('errors/401.html'), 401


@errors.app_errorhandler(403)
def error_403(error):
    """ Page loaded when 403 error occurs """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(404)
def error_404(error):
    """ Page loaded when 404 error occurs """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    """ Page loaded when 500 error occurs """
    return render_template('errors/500.html'), 500


@errors.app_errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    flash('There was an error on our end, try again and it should work', 'error')
    return redirect(url_for('main.homepage'))