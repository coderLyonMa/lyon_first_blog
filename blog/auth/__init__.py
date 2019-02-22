from flask import Blueprint

auth = Blueprint('auth', __name__)

from .import views
from blog.models import Permission

@auth.context_processor
def inject_permissions():
    return dict(Permission=Permission)