from flask import Flask
from routes.index import main as index_routes
from routes.api import main as api_routes
from config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    # 设置 secret_key 以使用 flask 自带的 session
    app.secret_key = SECRET_KEY
    app.register_blueprint(index_routes)
    app.register_blueprint(api_routes, url_prefix='/api')
    return app

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3001,
        threaded=True,
    )
    app = create_app()
    app.run(**config)

