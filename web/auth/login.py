from flask import render_template, redirect, url_for, request, session
from flask import Blueprint

from pref import Preferences

from sql.database import engine, init_db
from core.user import User

bp = Blueprint("auth", __name__, template_folder='templates', static_folder='static')


@bp.route('/', methods=["GET"])
def index():
    # Find user
    user_id = session.get("user_id")
    init_db(engine)
    user = User.find(user_id) if user_id else None

    if user:
        return redirect(url_for("quest_editor.quest_editor"))

    title = Preferences.app_name
    editor_version = '1.0'
    login_is_required = request.args.get("login_is_required")
    return render_template('index.html', title=title,
                           editor_version=editor_version, login_is_required=login_is_required)
