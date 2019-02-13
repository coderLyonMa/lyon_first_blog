from flask import Blueprint
from blog.models import Permission

main = Blueprint('main', __name__)

from . import views, errors

@main.context_processor
def inject_permissions():
    return dict(Permission=Permission)