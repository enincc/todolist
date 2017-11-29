// ------------------------- User API -------------------------
// 用 ajax 请求后端 api
// 
// user 注册
var apiUserRegister = function(form, callback) {
    var path = '/api/user/register'
    ajax('POST', path, form, callback)
}

// user 登录
var apiUserLogin = function(form, callback) {
    var path = '/api/user/login'
    ajax('POST', path, form, callback)
}

// user 登出
var apiUserLogout = function(callback) {
    var path = '/api/user/logout'
    ajax('GET', path, '', callback)
}

// 验证 user 是否登录
var apiUserLoggedIn = function(callback) {
    var path = '/api/user/logged_in'
    ajax('GET', path, '', callback)
}

// 修改密码
var apiUserUpdatePassword = function(form, callback) {
    var path = '/api/user/password/update'
    ajax('POST', path, form, callback)
}

// 新增分类
var apiUserAddCategory = function(form, callback) {
    var path = '/api/user/category/add'
    ajax('POST', path, form, callback)
}

// 删除分类
var apiUserDeleteCategory = function(form, callback) {
    var path = '/api/user/category/delete'
    ajax('POST', path, form, callback)
}

// 获取所有分类
var apiUserAllCategories = function(callback) {
    var path = '/api/user/category/all'
    ajax('GET', path, '', callback)
}

// ------------------------- DOM 节点模板 -------------------------
// 返回用于创建 DOM 节点的 HTML 字符串
//
// message DOM, 展示后端发回的提示
var messageTemplate = function(message) {
    var m = `
        <div class="alert alert-dismissible alert-${message[0]}">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            <p>${message[1]}</p>
        </div>
    `
    return m
}

// ------------------------- DOM 节点操作 -------------------------
// 
// 插入一条新的 message
var insertMessage = function (message) {
    var messageDiv = messageTemplate(message)
    // 插入 todo-list
    var todoList = e('#todo-list')
    todoList.insertAdjacentHTML('afterbegin', messageDiv)
}

// 插入一条新的 todo 分类
var insertCategory = function (category) {
    var categoriesMenu = e('#id-dropdown-categories .dropdown-menu')
    var c = `<li><a href="###">${category}</a></li>`
    categoriesMenu.insertAdjacentHTML('beforeend', c)

    var categorySelects = eAll('form select[name="category"]')
    var o = `<option>${category}</option>`
    var len = categorySelects.length 
    for (var i = 0; i < len; i++) {
        categorySelects[i].insertAdjacentHTML('beforeend', o)
    }
}

// 移除一条 todo 分类
var removeCategory = function (index, category) {
    var categoryLis = e('#id-dropdown-categories .dropdown-menu').childNodes
    var len = categoryLis.length
    for (var i = 2; i < len; i++) {
        if (categoryLis[i].innerText === category) {
            categoryLis[i].remove()
            break
        }
    }
      
    var categorySelects = eAll('form select[name="category"]')
    var len = categorySelects.length 
    for (var i = 0; i < len; i++) {
        categorySelects[i].remove(index)
    }
}

// ------------------------- 绑定事件 -------------------------
// 
// 监听注册按钮
var bindEventUserRegister = function() {
    var b = e('#id-button-register')
    b.addEventListener('click', function () {
        var f = e('#id-modal-register form')
        var form = {
            username: f.username.value,
            password: f.password.value,
        }
        f.reset()
        apiUserRegister(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var message = JSON.parse(r)
            insertMessage(message)
        })
    })
}

// 监听登录按钮
var bindEventUserLogin = function() {
    var b = e('#id-button-login')
    b.addEventListener('click', function () {
        var f = e('#id-modal-login form')
        var form = {
            username: f.username.value,
            password: f.password.value,
        }
        f.reset()
        apiUserLogin(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var message = JSON.parse(r)               
            insertMessage(message)
            if (message[0] === 'success') {
                location.reload()
            } 
        })
    })
}

// 监听登出按钮
var bindEventUserLogout = function() {
    var b = e('#id-logout')
    b.addEventListener('click', function () {
        apiUserLogout(function (r) {
            // 收到返回的数据, 插入到页面中
            var message = JSON.parse(r)               
            insertMessage(message)
            if (message[0] === 'success') {
                location.reload()
            } 
        })
    })
}

// 监听修改密码
var bindEventUpdatePassword = function() {
    var b = e('#id-button-password')
    b.addEventListener('click', function () {
        var f = e('#id-modal-password form')
        var form = {
            old_pwd: f.old_pwd.value,
            new_pwd: f.new_pwd.value,
        }
        f.reset()
        apiUserUpdatePassword(form, function (r) {
            // 收到返回的数据, 插入到页面中
            var message = JSON.parse(r)               
            insertMessage(message)
        })
    })
}

// 监听分类修改
var bindEventCategory = function() {
    var b = e('#id-button-category')
    b.addEventListener('click', function () {
        var tab = e('#id-modal-category .nav a[aria-expanded="true"]').innerText
        if (tab === '新增分类') {
            var f = e('#id-add-category form')
            var form = {
                category: f.category.value,
            }
            f.reset()
            apiUserAddCategory(form, function (r) {
                var message = JSON.parse(r)               
                insertMessage(message)
                if (message[0] === 'success') {
                    insertCategory(form.category)
                }
            })
        }
        if (tab === '删除分类') {
            var f = e('#id-delete-category form')
            var form = {
                category: f.category.value,
            }
            var index = f.category.selectedIndex
            f.reset()
            apiUserDeleteCategory(form, function (r) {
                var message = JSON.parse(r)               
                insertMessage(message)
                if (message[0] === 'success') {
                    removeCategory(index, form.category)
                }
            })
        }
    })
}

// 登陆时监听的事件
var bindEventsLoggedIn = function () {
    bindEventUserLogout()
    bindEventUpdatePassword()
    bindEventCategory()
}

// 未登陆时监听的事件
var bindEventsNotLoggedIn = function () {
    bindEventUserRegister()
    bindEventUserLogin()
}

var __main = function () {
    apiUserLoggedIn(function (r) {
        var message = JSON.parse(r) 
        if (message[0] === 'success') {
            bindEventsLoggedIn()
        } 
        else {
            bindEventsNotLoggedIn()
        }
    })
}

__main()