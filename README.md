# todolist
todolist 单页面应用，[Demo 地址](http://todo.enin.cc/)

- 基于 Flask 框架，数据库使用了 MongoDB，界面实现采用前端框架 Bootstrap 及其免费主题 Bootswatch。
- 实现功能：
    - 用户注册、登录、密码修改
    - 创建、修改和删除 Todo，支持 Markdown 语法
    - 根据分类筛选 Todo，支持新增或删除分类
### 演示
![演示图片](https://github.com/enincc/todolist/blob/master/todolist.gif)

### 运行和部署相关

- 安装依赖库 `pip install -r requirements.txt`

- 运行前需要在 `config.py` 文件中修改密钥、数据库名、展示用帐户、新用户初始化等配置选项，可参照 `config_copy.py` 自行创建。

- 部署使用了 Nginx + Supervisor + Gunicorn ，具体配置分别在 `todo.nginx`、`todo.conf` 及 `gunicorn.config.py` 中修改。

- `configuration\setup_development.sh` 和 `configuration\setup_production.sh` 分别是开发环境和生产环境部署脚本，可根据需要自行修改。

