import logging

from flask import render_template
from flask import Blueprint

from pref import Preferences


bp = Blueprint("errors", __name__)


""" LOGGING """
logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask Server")


@bp.errorhandler(404)
def page_not_found(e):
    logger.info(e)
    return render_template('404.html'), 404


@bp.errorhandler(500)
def page_not_found(e):
    logger.info(e)
    return render_template('500.html'), 500
