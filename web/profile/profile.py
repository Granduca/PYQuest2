from flask import render_template, redirect, url_for, request, session
from flask import Blueprint

from pref import Preferences

from sql.database import engine, init_db
from core.user import User

bp = Blueprint("profile", __name__, template_folder='templates', static_folder='static')


@bp.route('/', methods=["GET"])
def index():
    # Find user
    user_id = session.get("user_id")
    init_db(engine)
    user = User.find(user_id)

    if not user:
        return redirect(url_for("auth.index"))

    user_status = "Заслуженный автор и Бог"
    google_upic = session.get("google_upic", "default_pic.jpg")

    title = Preferences.app_name
    editor_version = '1.0'

    user_num_quests = 17
    user_num_readers = 567
    user_rating = 9.8

    return render_template('profile.html', title=title, editor_version=editor_version,
                           user_name=user.username, google_upic=google_upic, user_status=user_status,
                           user_num_quests=user_num_quests, user_num_readers=user_num_readers, user_rating=user_rating)
