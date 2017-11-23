import time
from models import Model


class Todo(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('task', str, ''),
            ('user_id', str, ''),
        ]
        return names

    @classmethod
    def update_date(cls, t_id, form):
        t = cls.find_by(id=t_id)
        t.task = form.get('task')
        t.update()
        return t

    def is_owner(self, u_id):
        return self.user_id == u_id
