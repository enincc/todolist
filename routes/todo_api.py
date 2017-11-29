from flask import (
    jsonify,
    Blueprint,
    request,
    g,
)
from models.todo import Todo
from models.user import User
from config import SAMPLE_USER
# api 只返回 json 格式的数据
main = Blueprint('todo_api', __name__)


@main.route('/all', methods=['GET'])
def all():
    # 返回全部 todo
    # 未登录时返回展示用帐号创建的 todo
    if g.user is None:
        u_id = User.find_by(username=SAMPLE_USER).id
    else:
        u_id = g.user.id
    ts = Todo.all_json(user_id=u_id)
    return jsonify(ts)


@main.route('/<int:t_id>', methods=['GET'])
def one(t_id):
    # 返回单个 todo
    if g.user is None:
        u_id = User.find_by(username=SAMPLE_USER).id
    else:
        u_id = g.user.id
    t = Todo.find_by(id=t_id, user_id=u_id)
    if t:
        return jsonify(t.json())
    else:
        return jsonify(['warning', '未登录。'])


@main.route('/add', methods=['POST'])
def add():
    # 获取浏览器请求附带的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 request.get_json 函数获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    t = Todo.new(form, user_id=g.user.id)
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())


@main.route('/delete', methods=['GET'])
def delete():
    t_id = int(request.args.get('id'))
    t = Todo.find_by(id=t_id)
    t.delete()
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
def update():
    form = request.get_json()
    t = Todo.update_date(form)
    return jsonify(t.json())


