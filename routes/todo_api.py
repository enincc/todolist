from flask import (
    jsonify,
    Blueprint,
    request,
)
from models.todo import Todo
# api 只返回 json 格式的数据
main = Blueprint('todo_api', __name__)


@main.route('/all', methods=['GET'])
def all():
    # 返回全部 todo
    ts = Todo.all_json()
    return jsonify(ts)


@main.route('/<int:t_id>', methods=['GET'])
def one(t_id):
    # 返回单个 todo
    t = Todo.find_by(id=t_id)
    return jsonify(t.json())


@main.route('/add', methods=['POST'])
def add():
    # 获取浏览器请求附带的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 request.get_json 函数获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    t = Todo.new(form)
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

