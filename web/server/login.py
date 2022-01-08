from flask import render_template, request
from flask import Blueprint

from pref import Preferences

bp = Blueprint("index", __name__)


@bp.route('/', methods=['GET'])
def index():
    login_is_required = ''
    if "login_is_required" in request.args:
        login_is_required = request.args['login_is_required']
    title = Preferences.app_name
    editor_version = '1.0'
    return render_template('index.html', title=title,
                           editor_version=editor_version, login_is_required=login_is_required)
