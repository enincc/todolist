from models import Model
from config import SALT_KEY
import hashlib


class User(Model):
    """
    User 保存用户数据的 models
    """
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('user_avatar', str, '/static/uploads/default.png'),
        ]
        return names

    @staticmethod
    def salted_password(password, salt=SALT_KEY):
        """
        加盐哈希，盐值salt用os.urandom(24)生成
        更安全的做法是给每个用户绑定一个随机的盐值
        """
        salted = salt + password
        hash_pwd = hashlib.sha256(salted.encode('utf-8')).hexdigest()
        return hash_pwd

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and len(pwd) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        user = User.find_by(username=name)
        if user is not None and user.password == user.salted_password(pwd):
            return user
        else:
            return None

    def update_avatar(self, filename):
        self.user_avatar = '/static/uploads/' + filename
        self.update()

    def update_password(self, form):
        if self.password == self.salted_password(form.get('old_pwd')) and len(form.get('new_pwd')) > 2:
            self.password = self.salted_password(form.get('new_pwd'))
            self.update()
            return True
        else:
            return False




