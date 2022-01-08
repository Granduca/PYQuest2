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


logging.basicConfig(level=Preferences.logging_level_core)
logger = logging.getLogger(f"{Preferences.app_name} Flask Google OAuth")

bp = Blueprint('google_auth', __name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.abspath(os.path.join(pathlib.Path(__file__).parent, "../secret/client_secret.json"))

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri="http://127.0.0.1:5000/google/callback"
)


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect(url_for('index', login_is_required='true'))  # Authorization required
        else:
            return function(*args, **kwargs)
    return wrapper


@bp.route("/google/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.route("/google/callback")
def callback():
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
        audience=flow.client_config['client_id']
    )

    session["google_id"] = id_info.get("sub")
    session["google_uname"] = id_info.get("name")
    session["google_upic"] = id_info.get("picture")

    return redirect("/quest_editor")


@bp.route("/google/logout")
def logout():
    session.clear()
    return redirect('/')
