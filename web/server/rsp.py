from flask import jsonify, make_response


class ServerResponse:
    def __init__(self):
        self._category = {
            'success': {
                'ok': 200,
            },
            'error': {
                'no_content': 204,
                'bad_request': 400,
                'unauthorized': 401,
                'forbidden': 404,
                'internal_server_error': 500
            },
            'info': {
                'accepted': 202,
            }
        }
        self._headers = "application/json"
        
    def response(self, category, status, **kwargs):
        msg = ""
        data = {}
        for arg in kwargs:
            if arg == 'msg':
                if isinstance(kwargs[arg], str):
                    msg = kwargs[arg]
                else:
                    return self.internal_server_error()

        if self._category[category] and self._category[category][status]:
            response = make_response(jsonify(message=msg, category=category, data=data, status=self._category[category][status]))
            response.headers["Content-Type"] = self._headers
            return response
        else:
            return self.internal_server_error()

    def internal_server_error(self, **kwargs):
        msg = 'Internal server error'
        for arg in kwargs:
            if arg == 'msg':
                if isinstance(kwargs[arg], str):
                    msg = f"{msg} [{kwargs[arg]}]"
        response = make_response(jsonify(message=msg, category='error', status=self._category['error']['internal_server_error']))
        response.headers["Content-Type"] = self._headers
        return response
