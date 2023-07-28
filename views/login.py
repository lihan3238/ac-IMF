"""
login.py 是一个 Flask 蓝图（Blueprint）模块，包含与用户登录相关的视图函数。
这些视图函数用于处理用户登录的 HTTP 请求，并返回相应的页面或数据。
通过装饰器 @login.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

在登录过程中，首先通过表单 LoginForm 验证用户提交的登录信息。
然后，通过调用 User 模型的 get_by 方法根据用户名和哈希密码获取用户对象，
如果用户对象存在，则登录成功，并调用 OnlineUser 模型的 create_record 方法创建在线用户记录，
并返回一个 token。最后，将 token 存入响应头中，并重定向到根路由 /，
完成用户登录。如果登录失败，则在登录页面显示错误消息。
"""


# 导入需要的模块和函数
from flask import Blueprint, render_template, redirect
from form import LoginForm
from common import *

# 创建名为 'login' 的 Flask 蓝图
login = Blueprint('login', __name__)

# 定义处理根路由（'/login'）的视图函数，用于显示登录页面


@login.route('/')
def get__login():
    # 渲染 login.html 模板并传递 LoginForm 表单对象
    return render_template('login.html', form=LoginForm())

# 定义处理根路由（'/login'）POST 请求的视图函数，用于处理用户登录的逻辑


@login.route('/', methods=['POST'])
def post__login():
    # 导入 User 和 OnlineUser 模型
    from models import User, OnlineUser

    try:
        # 创建 LoginForm 表单对象并验证提交的数据
        form = LoginForm()
        # assert form.validate_on_submit(), 'invalid form fields'
        assert form.is_submitted() and form.validate(),'invalid form fields'
        # 获取表单中的哈希密码和用户名
        hash_password = form.get_hash_password()
        username = form.username.data

        # 调用 User 模型的 get_by 方法，根据用户名和哈希密码获取用户对象
        user = User.get_by(username=username, hash_password=hash_password)

        # 检查用户对象是否存在，如果不存在则抛出异常
        assert user, 'incorrect username or password'

        # 调用 OnlineUser 模型的 create_record 方法，创建在线用户记录，并获取对应的 token
        token = OnlineUser.create_record(user.id_)

        # 将 token 存入响应头中，并重定向到根路由 '/'
        return set_token(redirect('/'), token)

    except AssertionError as e:
        # 如果登录失败，获取异常消息，并将消息传递给 login.html 模板进行显示
        message = e.args[0] if len(e.args) else str(e)
        return render_template('login.html', form=LoginForm(), message=message)
