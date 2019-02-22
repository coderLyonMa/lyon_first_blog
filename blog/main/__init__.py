from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

@main.context_processor
def inject_permissions():
    return dict(Permission=Permission)