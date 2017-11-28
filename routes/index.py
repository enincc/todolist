from flask import (
    render_template,
    Blueprint,
    g,
)
from auth import current_user


main = Blueprint('index', __name__)


@main.before_app_request
def before_request():
    """
    每次请求之前把g.user设为当前用户
    """
    g.user = current_user()


@main.route('/')
def index():
    return render_template('base.html')
