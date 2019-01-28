from flask import session, url_for, redirect, render_template, current_app
from .. import db
from datetime import datetime
from ..models import User, Role
from .forms import NameForm
from ..email import send_email
from . import main


@main.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['ADMIN_MARIO']:
                send_email(current_app.config['ADMIN_MARIO'], 'New User!',
                           "mail/new_user", user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', name=session.get('name'), form=form,
            known=session.get('known', False), current_time=datetime.utcnow())