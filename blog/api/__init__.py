from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentification, posts, users, comments, errors