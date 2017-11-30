// ------------------------- ToDoList API -------------------------
// 用 ajax 请求后端 api
// 
// 获取所有 todo
var apiTodoAll = function (callback) {
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

// 用 id 获取单个 todo
var apiTodoOne = function (id, callback) {
    var path = '/api/todo/' + id
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function (form, callback) {
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

// 删除一个 todo
var apiTodoDelete = function (id, callback) {
    var path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
}

// 修改一个 todo
var apiTodoUpdate = function (form, callback) {
    var path = '/api/todo/update'
    ajax('POST', path, form, callback)
}


// ------------------------- DOM 节点模板 -------------------------
// 返回用于创建 DOM 节点的 HTML 字符串
// 
// TODO DOM
var todoTemplate = function (todo) {
    var title = todo.title
    var content = marked(todo.content)
    var id = todo.id
    var updated_time = timeString(todo.updated_time)
    var category = todo.category
    // data-* 是 HTML5 自定义标签属性
    // 若 data-id="1"，获取属性的方式是 .dataset.id
    var t = `
        <div class="col-sm-3 todo-cell" data-id="${id}">
        <div class="panel panel-default">
            <div class="panel-heading">
                <span class="pull-right">
                    <a href="###"><span class="glyphicon glyphicon-edit text-muted todo-edit" data-id="${id}" title="编辑" data-toggle="modal" data-target="#id-modal-edit"></span></a>
                    <a href="###"><span class="glyphicon glyphicon-trash text-muted todo-delete" data-id="${id}" title="删除"></span></a>
                </span>
                ${title}
            </div>
            <div class="panel-body">
                <small class="text-muted"><div class="todo-info">
                    <span class="pull-right">分类：<span class="todo-category">${category}</span></span>
                    <span>${updated_time}</span></div>
                </small>
                <div class="markdown-body">${content}</div>
            </div></div>
        </div>
    `
    return t
}


// ------------------------- DOM 节点操作 -------------------------
// 
// 插入一个新的 todo
var insertTodo = function (todo) {
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('#todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

// 替换一个 todo
var replaceTodo = function (todo) {
    var newTodoCell = todoTemplate(todo)
    // 插入 todo-list
    var oldTodoCell = e(`.todo-cell[data-id="${todo.id}"]`)
    oldTodoCell.insertAdjacentHTML('afterend', newTodoCell)
    oldTodoCell.remove()
}

// 载入全部 todo
var loadTodos = function () {
    // 调用 ajax api 来载入数据
    apiTodoAll(function (r) {
        // 解析为 数组
        var todos = JSON.parse(r)
        // 循环添加到页面中
        for (var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}


// ------------------------- 绑定事件 -------------------------
// 
var bindEventTodoAdd = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        var f = e('#id-modal-add form')
        var form = {
            title: f.title.value,
            content: f.content.value,
            category: f.category.value,
        }
        f.reset()
        apiTodoAdd(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r)
            if (todo[0] === 'warning') {
                // insertMessage(todo)
                insertTodo(form)
            } else {
                insertTodo(todo)
            }
        })
    })
}

var bindEventTodoDelete = function () {
    var todoList = e('#todo-list')
    todoList.addEventListener('click', function (event) {
        // 通过 event.target 得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class 判断元素是否我们想要的
        // classList 属性保存了元素所有的 class
        if (self.classList.contains('todo-delete')) {
            // log('点击 删除按钮')
            var todoId = self.dataset.id
            apiTodoDelete(todoId, function (r) {
                // log('服务器响应删除成功', r)
                // 收到返回的数据, 删除 self 所在的 todo-cell 节点
                self.closest('.todo-cell').remove()
            })
        }
    })

}

var bindEventTodoEdit = function () {
    var todoList = e('#todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-edit')) {
            var todoId = self.dataset.id
            apiTodoOne(todoId, function (r) {
                var todo = JSON.parse(r)
                var form = e('#id-modal-edit')
                form.querySelector('input[name="id"]').value = todo.id
                form.querySelector('input[name="title"]').value = todo.title
                form.querySelector('select[name="category"]').value = todo.category
                form.querySelector('textarea').value = todo.content
            })
        }
    })
}

var bindEventTodoUpdate = function () {
    var b = e('#id-button-update')
    b.addEventListener('click', function () {
        var f = e('#id-modal-edit form')
        var form = {
            id: f.id.value,
            title: f.title.value,
            content: f.content.value,
            category: f.category.value,
        }
        f.reset()
        apiTodoUpdate(form, function (r) {
            var todo = JSON.parse(r)
            if (todo[0] === 'warning') {
                insertMessage(todo)
                replaceTodo(form)
            } else {
                replaceTodo(todo)
            }       
        })
    })
}

// 监听分类选择
var bindEventTodoFilter = function () {
    var categoriesMenu = e('#id-dropdown-categories .dropdown-menu')
    categoriesMenu.addEventListener('click', function (event) {
        var category = event.target.innerText
        e('#id-filter-category').innerText = category
        var todoCells = eAll('.todo-cell')
        var len = todoCells.length
        for (var i = 0; i < len; i++) {
            var todoCell = todoCells[i]
            var todoCategory = todoCell.querySelector('.todo-category').innerText
            if (category === '全部' || category === todoCategory) {
                todoCell.style.display = ''
            } else {
                todoCell.style.display = 'none'
            }
        }
    })
}


var bindEvents = function () {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
    bindEventTodoFilter()
}

var __main = function () {
    bindEvents()
    loadTodos()
}

__main()


