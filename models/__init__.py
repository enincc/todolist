import time
from math import ceil
from pymongo import MongoClient
from config import DATABASE_NAME

client = MongoClient()
# 此处设置数据库的名字
db = client[DATABASE_NAME]


def next_id(name):
    """
    用计数器集合在MongoDB中模拟自增id
    """
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 集合 data_id 存储其他集合的最新 id
    doc = db['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Model(object):
    # 设置每页显示的数量
    page_size = 20

    @classmethod
    def valid_names(cls):
        names = [
            '_id',
            # (字段名, 类型, 值)
            ('id', int, -1),
            ('deleted', bool, False),
            ('created_time', int, 0),
            ('updated_time', int, 0),
        ]
        return names

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        外部调用 new 方法新增数据
        """
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        names = cls.valid_names().copy()
        # 去掉 _id 这个特殊的字段
        names.remove('_id')
        if form is None:
            form = {}

        for f in names:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.deleted = False
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        给查找方法从内部使用
        从 mongo 数据中恢复一个 models
        """
        m = cls()
        names = cls.valid_names().copy()
        # 去掉 _id 这个特殊的字段
        names.remove('_id')
        for f in names:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        # _id 加回去，否则会生成一个新的 _id
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def _cursor(cls, **kwargs):
        name = cls.__name__
        kwargs['deleted'] = False
        sort = kwargs.pop('__sort', None)
        page = kwargs.pop('__slice', None)
        distinct = kwargs.pop('__distinct', None)
        ds = db[name].find(kwargs)
        if distinct is not None:
            dl = ds.distinct(distinct)
            dl.reverse()
            if page is not None:
                dl = dl[page[0]: page[1]]
            return dl
        if sort is not None:
            ds = ds.sort(*sort)
        if page is not None:
            ds = ds.limit(page[1]-page[0]).skip(page[0])
        return ds

    @classmethod
    def _find(cls, **kwargs):
        """
        mongo 数据查询
        """
        ds = cls._cursor(**kwargs)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_by(cls, **kwargs):
        return cls._find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        """
        __sort=(<string: key>, <int: direction>)
            根据 key 排序，direction为1时升序，-1降序
        """
        return cls._find(**kwargs)

    @classmethod
    def find_page(cls, page=1, page_size=page_size, **kwargs):
        """
        分页查询
        __slice=[<int: begin>, <int: end>]
            对查询结果进行分片
        """
        kwargs['__slice'] = [(page - 1) * page_size, page * page_size]
        return cls._find(**kwargs)

    @classmethod
    def find_distinct(cls, key, page=1, page_size=page_size, **kwargs):
        """
        ____distinct=<string: key>
            根据 key 去重，返回 key 的唯一值列表
        """
        kwargs['__distinct'] = key
        kwargs['__slice'] = [(page - 1) * page_size, page * page_size]
        return cls._cursor(**kwargs)

    @classmethod
    def _find_one(cls, **kwargs):
        """
        """
        ds = cls._cursor(**kwargs)
        for d in ds.limit(-1):
            m = cls._new_with_bson(d)
            return m
        return None

    @classmethod
    def count(cls, **kwargs):
        """
        文档总数
        """
        ds = cls._cursor(**kwargs)
        if isinstance(ds, list):
            return len(ds)
        else:
            return ds.count()

    @classmethod
    def pages(cls, **kwargs):
        """
        文档页数
        """
        pages = ceil(cls.count(**kwargs) / cls.page_size)
        return pages

    def save(self):
        """
        保存到数据库但不更新时间
        """
        name = self.__class__.__name__
        db[name].save(self.__dict__)

    def update(self):
        """
        保存到数据库并更新时间
        """
        self.updated_time = int(time.time())
        self.save()

    def delete(self):
        """
        删除，将 'deleted' 值设为 True
        原数据在数据库中仍然存在，只是无法通过 Model 提取
        """
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            '$set': {
                'deleted': True
            }
        }
        db[name].update_one(query, values)

    @staticmethod
    def blacklist():
        b = [
            '_id',
            'deleted',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    @classmethod
    def all_json(cls, **kwargs):
        ms = cls.find_all(**kwargs)
        js = [m.json() for m in ms]
        return js
