from flask import Flask, jsonify, Response ,render_template
from flask_cors import CORS

from src.config import config
from src.config.codingsphereslogger import logger
from src.helpers import *
# from trepan.api import debug
import ujson
import os
import re
import socket
from flask_mongoengine import MongoEngine
from flasgger import Swagger, swag_from

def strip_sensitive_data_for_sentry(event, hint):
  if event.get("request", {}).get("headers", {}).get("X-Api-Token"):
    event["request"]["headers"]["X-Api-Token"] = "__HIDDEN_TOKEN__"

  if "tokens" in event["request"].get("url") and event["request"].get("method") in ["GET", "PATCH"]:
    event["request"]["url"] = re.sub("(\/tokens\/)\w+", "/tokens/__HIDDEN_TOKEN__", event["request"]["url"])

  return event


app = Flask("codingspheres")


# app = Flask(__name__)
# connect(host="mongodb+srv://96vksingh:wcfyLqyKyqDsPj4u@cluster0.ksemp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# MongoDB Atlas configuration
app.config["MONGODB_SETTINGS"] = {
    "host": DB,
    "tls": True,  # Enforce TLS/SSL
    "tlsAllowInvalidCertificates": False  # Ensure certificate validity
}

# Enable CORS only for allowed FQDNs
if isinstance(config.WHITE_LISTED_CORS_ORIGINS, str):
  config.WHITE_LISTED_CORS_ORIGINS = config.WHITE_LISTED_CORS_ORIGINS.split(",")

CORS(app, origins = config.WHITE_LISTED_CORS_ORIGINS)
# logging.getLogger("mongoengine").setLevel(logging.WARNING)
# swagger UI is available at /apidocs/index.html
app.config['SWAGGER'] = {
    "swagger_version": "3.0.1",
    "uiversion": 3,  # Ensures the Swagger UI loads
    "specs": [
        {
            "version": "1.0",
            "title": "Codingspheres APIs",
            "description": "Provides APIs documentation",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

Swagger(app = app, template_file = "swagger.yml")

# Load config to app
app.config.from_pyfile("src/config/config.py")

db = MongoEngine(app)

# wires up controller routes
import src.controllers

@app.before_request
def log_calls():
  """
  Log the calls in stdout, if debug mode is enabled
  """
  try:
    print("Starting")
    if len(request.get_data()) == 0:
      msg = "ENDPOINT={} METHOD={} PAYLOAD=None".format(request.url, request.method)
    else:
      pload = request.get_json()
      if "password" in pload:
        msg = "ENDPOINT={} METHOD={} PAYLOAD=Obfuscated".format(request.url, request.method)
      else:
        msg = "ENDPOINT={} METHOD={} PAYLOAD='{}'".format(request.url, request.method, pload)
    logger.debug(msg)
  except Exception as e:
    logger.error(str(e))


@app.route('/apis/')
def swagger_ui():
    """
    Serve Swagger UI manually.
    """
    return render_template('index.html')

@app.route("/", methods=["GET", "OPTIONS"])
def root_uri():
  return responsify({"message": "Hello Its me Vishal. You need to authenticate yourself to use this service."})
# Handle all error cases
@app.errorhandler(404)
def error_400(error):
  return errorit("No such endpoint found", "UNKNOWN_ENDPOINT", 404)

@app.errorhandler(405)
def error_405(error):
  return errorit("The method is not allowed for the requested URL", "METHOD_NOT_ALLOWED", 405)

@app.errorhandler(500)
def error_500(error):
  return errorit("The server encountered an internal error and was unable to complete your request.", "INTERNAL_SERVER_ERROR", 500)

