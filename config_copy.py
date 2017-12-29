# 用于 Flask 框架的密钥，用于 session 加密，用os.urandom(24)生成
SECRET_KEY = '\x98y\xf4jU\xad\xe1\x08Z)\x08\x17\x07\n\x1d\x16\xcb\xe6\xd3xJx\xebH'
# 给用户密码哈希加密所用的盐(salt)值，用os.urandom(24)生成
SALT_KEY = '\x84\xcf\xe2\xa1\x11QH[\x8f\x92j\xba4\x9e\x0bd\x13\x1c\xbeb\x14\x05\x9f\xb3'
# 数据库名
DATABASE_NAME = 'bbs'
# 展示用帐号的 username, 该帐号创建的 ToDo 将会展示给未登录用户
SAMPLE_USER = 'admin'
# 为每个新用户创建的初始化 ToDo
FORMS = [
    {
        'title': '关于本站',
        'category': '其他',
        'content': """### 关于 ###
- 本站是基于 AJAX  实现的 TodoList 单页面应用
- [源码地址](https://github.com/enincc/todolist)

### 作者的其他项目 ###
- [社区](http://www.enin.cc/)
- [聊天室](http://chat.enin.cc/)""",
    },
    {
        'title': 'Markdown 示范',
        'category': '学习',
        'content': """
- \### 单行的标题
### 单行的标题
- \*\*粗体\*\* \*斜体\* \*\*\*粗斜体\*\*\*
**粗体** *斜体* ***粗斜体***
- \`console.log('行内代码')\`
`console.log('行内代码')`
- \```js code \``` 标记代码块
```js code ```
- \[链接名称](链接网址)
 [Markdown 编辑器语法指南](https://segmentfault.com/markdown)
- \!\[图片名称](图片网址)
![图片名称](https://www.baidu.com/img/baidu_jgylogo3.gif)""",
    },
]
