from pref import Preferences

import os
import pathlib
from functools import wraps
import logging

from flask import Blueprint, session, abort, redirect, request, url_for

import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from sql.database import engine, init_db
from core.user import User


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask Google OAuth")

bp = Blueprint('google', __name__, template_folder='quest_editor/templates', static_folder='quest_editor/static')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.abspath(os.path.join(pathlib.Path(__file__).parent, "secret/client_secret.json"))

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri="http://127.0.0.1:5000/auth/google/callback"
)


def sync_time(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        time_offset = 0
        try:
            import ntplib
            ntpc = ntplib.NTPClient()
            response = ntpc.request('europe.pool.ntp.org', version=3)
        except Exception as e:
            logger.error(e)
            abort(500)
        else:
            if response.offset > 0:
                import time
                logger.warning('Local clock synchronization required')
                time_offset = response.offset
        
        return function(*args, time_offset=time_offset, **kwargs)
    return wrapper


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        # Find user
        user_id = session.get("user_id")
        init_db(engine)

        if user_id:
            user = User.find(user_id)
            if user:
                logger.debug(f"User found: {user}")
                return function(*args, **kwargs)
            else:
                logger.warning(f"User session is not empty, but user {user_id} doesn't exist")

        logger.debug("User session is empty")
        return redirect(url_for('auth.index', login_is_required='true'))  # Authorization required

    return wrapper


@bp.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.route("/callback")
@sync_time
def callback(**kwargs):
    time_offset = kwargs.get("time_offset", 0)

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=flow.client_config['client_id'],
        clock_skew_in_seconds=time_offset
    )

    # Store google information
    google_id = id_info.get("sub")
    google_uname = id_info.get("name")

    if google_id:
        # Find or create user
        init_db(engine)
        user = User.query.filter_by(google_id=google_id).one_or_none()
        if not user:
            user = User.create(google_id=google_id, username=google_uname)
            logger.info(f"New user is created: {user}")
        else:
            logger.debug(f"User is found: {user}")

        session["user_id"] = user.id
        session["google_upic"] = id_info.get("picture")

    return redirect(url_for("auth.index"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
