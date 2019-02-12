from flask import session, url_for, redirect, render_template, current_app
from .. import db
from datetime import datetime
from ..models import User, Role
from .forms import NameForm
from ..email import send_email
from . import main


@main.route('/')
def index():
    return render_template('index.html')