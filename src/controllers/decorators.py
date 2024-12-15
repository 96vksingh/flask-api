import uuid

from functools import wraps

from flask import request, g, has_request_context
from requests import codes
from src.helpers import errorit

class ERROR_RESPONSE_CODES:
  BAD_JSON = "BAD_JSON"
  MISSING = "RESOURCE_DOES_NOT_EXIST"
  USER_REQUIRED = "USER_LOGIN_REQUIRED"
  ACCESS_DENIED = "ACCESS_DENIED"

def json_payload_required(view_func):

  @wraps(view_func)
  def decorated_function(*args, **kwargs):
    assert has_request_context()

    try:
      data = request.get_json()
    except:
      return errorit("unable to parse json", ERROR_RESPONSE_CODES.BAD_JSON, codes.bad_request)

    if not data:
      return errorit("missing json", ERROR_RESPONSE_CODES.BAD_JSON, codes.bad_request)

    return view_func(*args, **kwargs)

  return decorated_function
