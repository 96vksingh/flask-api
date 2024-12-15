import datetime

import ujson

from flask import Response, jsonify, request, g
from parse import *

from src.config.config import *


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%SZ')

def errorit(msg, custom_code, http_code=400, info="", mimetype="application/json", debug_info=None, **kwargs):
  """
  An utility for returning error reponse of an api call

  :param  msg: [string or array] e.g. "user not found"
  :param  custom_code: [string] e.g. USER_NOT_FOUND
  :param  http_code: [integer]
  :param  info: [string] e.g. For more info visit xyz.com/eww
  :param  mimetype: [integer]
  :param  debug_info: [dictionary] - any data to be returned
  :param kwargs: [dictionary] - custom data
  :return [Object] Response object
  """
  return Response(
    response=err_dict(msg, custom_code, ( "{}{}".format(API_URI, info) if info else ""), debug_info, **kwargs),
    status=http_code,
    mimetype=mimetype
  )


def responsify(payload, links={}, http_code=200, mimetype="application/json"):
  """
  An utility for returning reponse of an api call

  :param  payload: [dictionary] e.g. {"name": "john"}
  :param  links: [dictionary] e.g. {"movie_url": "http://sdsd.com/232/movie.html"}
  :param  http_code: [integer]
  :param  mimetype: [string]

  :return [Object] Response object
  """
  if payload is not None and links:
    payload["links"] = links

  data = ujson.dumps(payload, default=myconverter) if payload is not None else None

  return Response(
    response=data,
    status=http_code,
    mimetype=mimetype
  )

def err_dict(msg, code, info="", debug_info=None, **kwargs):
  """
  An utility for building error json

  :param  msg: [array] e.g. "user not found"
  :param  code: [string] e.g. USER_NOT_FOUND
  :param  info: [string] e.g. For more info visit xyz.com/eww
  :param  debug_info: [dictionary] - any data to be returned

  :return [String] json
  """

  if not isinstance(msg, list): # convert message to an array, if it is not
    msg = [msg]

  dc = {
    "errors": msg,
    "code": code,
    **kwargs
  }

  if not code:
    dc.pop("code")
  if info:
    dc.update({"info": info})
  if debug_info:
    dc.update({"debug_info": debug_info})

  dc["service"] = SERVICE_ID

  return ujson.dumps(dc)

