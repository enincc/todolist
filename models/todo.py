import time
from models import Model


class Todo(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            'task',
            'user_id',
        ]
        return names

    @classmethod
    def update(cls, id, form):
        m = super().update(id, form)
        m.updated_time = int(time.time())
        m.save()
        return m

    def is_owner(self, id):
        return self.user_id == id
