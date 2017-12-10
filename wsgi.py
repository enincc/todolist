#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app


# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))
# gunicorn 必须有一个叫做 application 的变量，变量的值是 Flask 实例
application = app.create_app()

