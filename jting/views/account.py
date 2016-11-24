# coding: utf-8

from flask import Blueprint
from flask import request, url_for, session
from flask import abort, redirect, render_template
from jting.libs.cache import redis
from jting.libs.utils import full_url
from jting.models import User, UserSession
from jting.forms import (
    Form,
    RegisterForm,
    PasswordForm,
    EmailForm, LoginForm,
)

bp = Blueprint('account', __name__, template_folder='templates')

@bp.route('/settings')
def user_settings():
    return 'Not Ready'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        UserSession.login(form.user, True)
        next_url = request.args.get('next_url', '/')
        return redirect(next_url)
    return render_template('account/login.html', form=form)

