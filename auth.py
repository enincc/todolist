from flask import (
    session,
    request,
    g,
    jsonify,
)
from models.user import User
from models.todo import Todo
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
            return jsonify(['warning', '请先登录'])
        else:
            return f(*args, **kwargs)
    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token', None)
        if token == session.get('token', -1):
            return f(*args, **kwargs)
        else:
            return jsonify(['warning', '403, 需要 Token'])
    return decorated_function


def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        models = {
            'todo_api': Todo,
        }
        # 根据蓝图名选择对应的 model
        model = models.get(request.blueprint)
        m_id = int(request.values.get('id') or request.get_json().get('id'))
        m = model.find_by(id=m_id)
        u = g.user
        if m.user_id == u.id:
            return f(*args, **kwargs)
        else:
            return jsonify(['warning', '403, 不是创建者'])
    return decorated_function
