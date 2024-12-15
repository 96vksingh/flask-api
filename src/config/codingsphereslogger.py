"""
Expose a global logger
And add request id with every call to help in debugging process
"""
import uuid
import flask
import logging
import logging.config
from src.config.config import LOG_LEVEL

def generate_request_id(original_id=""):
  """
  Generate a new request ID, optionally including an original request ID

  :param  original_id: [integer]

  :return [Object] Response object
  """
  new_id = uuid.uuid4()
  if original_id:
    new_id = "{},{}".format(original_id, new_id)

  return new_id
def request_id():
  """
  Returns the current request ID or a new one if there is none
  In order of preference:
    * If we've already created a request ID and stored it in the flask.g context local, use that
    * If a client has passed in the X-Request-Id header, create a new ID with that prepended
    * Otherwise, generate a request ID and store it in flask.g.request_id
  """
  if getattr(flask.g, "request_id", None):
    return flask.g.request_id

  headers = flask.request.headers
  original_request_id = headers.get("X-Request-Id")
  new_uuid = original_request_id if original_request_id else generate_request_id()
  flask.g.request_id = new_uuid

  return new_uuid

class RequestIdFilter(logging.Filter):
  """
  This is a logging filter that makes the request ID available for use in
  the logging format. Note that we're checking if we're in a request
  context, as we may want to log things before Flask is fully loaded.
  http://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html
  """
  def filter(self, record):
    record.request_id = request_id() if flask.has_request_context() else ""
    return True

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,  # Keep other loggers active
    "filters": {
        "request_id": { "()": RequestIdFilter }
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [RequestID: %(request_id)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            # "level": LOG_LEVEL,
            "level": "INFO",
            "formatter": "standard",
            "filters": ["request_id"]
        }
    },
    "root": {
        "handlers": ["console"],
        # "level": LOG_LEVEL
        "level": "INFO"
    }
})

logger = logging.getLogger("codingspheres")

