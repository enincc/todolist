# 防火墙
apt-get install ufw
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw enable

# 装依赖
apt-get update
apt-get install -y python3 python3-pip zsh
apt-get install -y git supervisor nginx mongodb
# 安装 oh-my-zsh 配置 (方便你使用命令行的配置)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# 安装开发库
pip3 install -U pip setuptools wheel
pip3 install jinja2 flask gunicorn pymongo
# pip3 install eventlet flask-socketio

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /root/todolist/todo.conf /etc/supervisor/conf.d/todo.conf
# 不要在 sites-available 里面放任何东西
ln -s -f /root/todolist/todo.nginx /etc/nginx/sites-enabled/todo

# 设置文件夹权限给 nginx 用
chmod o+rx /root
chmod -R o+rx /root/todolist

# 重启服务器
service supervisor restart
service nginx restart

echo 'setup production enviroment success'