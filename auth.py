from flask import (
    session,
    redirect,
    url_for,
    request,
    g,
    flash,
    abort,
)
from models.user import User
from functools import wraps


def current_user():
    """
    返回当前用户，未登录返回 None
    """
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('请先登录', 'error')
            return redirect(url_for('index.login'))
        return f(*args, **kwargs)
    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.values.get('token', None)
        if token == session.get('token', -1):
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorated_function
