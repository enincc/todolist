import time
from models import Model


class Todo(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('category', str, ''),
        ]
        return names

    @classmethod
    def update_date(cls, form):
        t_id = int(form.get('id'))
        t = cls.find_by(id=t_id)
        t.title = form.get('title')
        t.content = form.get('content')
        t.update()
        return t

    def is_owner(self, u_id):
        return self.user_id == u_id
