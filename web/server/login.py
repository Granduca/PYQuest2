from flask import render_template, redirect, request, session
from flask import Blueprint

from pref import Preferences

from sql.database import engine, init_db
from core.user import User

bp = Blueprint("index", __name__)


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=["GET"])
def index():
    # Find user
    user_id = session.get("user_id")
    init_db(engine)
    user = User.find(user_id)

    if user:
        return redirect("/quest_editor")

    title = Preferences.app_name
    editor_version = '1.0'
    login_is_required = request.args.get("login_is_required")
    return render_template('index.html', title=title,
                           editor_version=editor_version, login_is_required=login_is_required)
