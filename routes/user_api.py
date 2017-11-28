from flask import (
    jsonify,
    Blueprint,
    request,
    session,
    g,
)
import uuid
from models.user import User

main = Blueprint('user_api', __name__)


@main.route('/register', methods=['Post'])
def register():
    form = request.get_json()
    u = User.register(form)
    if u is not None:
        alert = ['success', '注册成功，请登录。']
    else:
        alert = ['warning', '注册失败，用户名可能已被占用，或用户名和密码不合法。']
    return jsonify(alert)


@main.route('/login', methods=['Post'])
def login():
    form = request.get_json()
    u = User.validate_login(form)
    if u is None:
        alert = ['warning', '登录失败，用户名或密码错误。']
    else:
        alert = ['success', '登录成功，欢迎。']
        # session 中写入 user_id 和 token
        session['user_id'] = u.id
        session['token'] = str(uuid.uuid4())
        # 设置 cookie 有效期为 持久，默认过期时间1个月，可通过app.permanent_session_lifetime修改
        session.permanent = True
    return jsonify(alert)


@main.route('/logout')
def log_out():
    # session.pop('user_id', None)
    session.clear()
    alert = ['success', '登出成功，再见。']
    return jsonify(alert)


@main.route('/logged_in')
def logged_in():
    if g.user is None:
        alert = ['warning', '未登录。']
    else:
        alert = ['success', '已登录。']
    return jsonify(alert)


@main.route('/password/update', methods=['Post'])
def update_password():
    u = g.user
    form = request.get_json()
    if u.update_password(form):
        alert = ['success', '密码修改成功。']
    else:
        alert = ['warning', '密码修改失败，当前密码错误，或新密码不合法。']
    return jsonify(alert)


@main.route('/category/add', methods=['Post'])
def add_category():
    u = g.user
    form = request.get_json()
    if u.add_category(form):
        alert = ['success', '分类添加成功。']
    else:
        alert = ['warning', '分类添加失败，分类为空或已存在。']
    return jsonify(alert)