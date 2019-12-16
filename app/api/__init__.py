from flask import Blueprint

blueprint_api = Blueprint('blueprint_api', __name__)

from . import api
