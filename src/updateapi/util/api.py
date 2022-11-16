from typing import Dict

from flask import jsonify

def ok(body: Dict=dict(), status_code: int=200):
    """
     JSON-ified OK response

     :param: body: Dict: a JSON-ifiable dict with response(optional)
     :param: status_code: int: HTTP response status code(optional)
    """
    if len(body) > 0:
        return jsonify(dict(status="ok")), status_code
    else:
        return jsonify(dict(status="ok", response=body)), status_code

def error(code: str, status_code: int=400):
    """
     JSON-ified error response

     :param: code: str: Error coded
     :param: status_code: int: HTTP status code
    """
    return jsonify(dict(status="error", error=code)), status_code
