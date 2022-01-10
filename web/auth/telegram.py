import hashlib
import hmac

from flask import redirect, request, jsonify
from flask import Blueprint
from flask import current_app

bp = Blueprint("telegram", __name__)


def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        string_arr.append(key + '=' + data[key])
    string_cat = '\n'.join(string_arr)
    return string_cat


@bp.route('/login')
def login():
    tg_data = {
        "id": request.args.get('id', None),
        "first_name": request.args.get('first_name', None),
        "last_name": request.args.get('last_name', None),
        "username": request.args.get('username', None),
        "auth_date": request.args.get('auth_date', None),
        "hash": request.args.get('hash', None)
    }
    print(tg_data)
    print(current_app.config['BOT_TOKEN'])
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(current_app.config['BOT_TOKEN'].encode('utf-8')).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string, 'utf-8')
    hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
    if hmac_string == tg_data['hash']:
        return redirect('/dashboard')

    return jsonify({
        'hmac_string': hmac_string,
        'tg_hash': tg_data['hash'],
        'tg_data': tg_data
    })
