from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """ Page loaded when 404 error occurs """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    """ Page loaded when 500 error occurs """
    return render_template('errors/500.html'), 500