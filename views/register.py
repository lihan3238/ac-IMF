"""
register.py 是一个 Flask 蓝图（Blueprint）模块，包含与用户注册相关的视图函数。
这些视图函数用于处理用户注册的 HTTP 请求，并返回相应的页面或数据。
通过装饰器 @register.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

在注册过程中，首先通过表单 RegisterForm 验证用户提交的注册信息。
然后，检查用户名和密码是否满足指定的格式要求，如果不满足则抛出异常并返回相应的错误消息。
最后，调用 User 模型的 create_user 方法创建用户并将用户信息存入数据库，
注册成功后重定向到登录页面 '/login'。如果注册失败，则在注册页面显示错误消息。
"""




# 导入需要的模块和函数
from flask import Blueprint, render_template, redirect
import re
from form import RegisterForm

# 创建名为 'register' 的 Flask 蓝图
register = Blueprint('register', __name__)

# 正则表达式，用于验证用户名和密码格式
username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]+')
password_pattern = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,36}')

# 定义处理根路由（'/register'）的视图函数，用于显示注册页面
@register.route('/')
def get__register():
    # 渲染 register.html 模板并传递 RegisterForm 表单对象
    return render_template('register.html', form=RegisterForm())

# 定义处理根路由（'/register'）POST 请求的视图函数，用于处理用户注册的逻辑
@register.route('/', methods=['POST'])
def post__register():
    # 导入 User 模型
    from models import User

    try:
        # 创建 RegisterForm 表单对象并验证提交的数据
        form = RegisterForm()
        #assert form.validate_on_submit(), 'invalid form fields'
        assert form.is_submitted() and form.validate(),'invalid form fields'
        # 获取表单中的用户名和密码
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # 检查用户名是否满足指定的格式，如果不满足则抛出异常
        assert username_pattern.fullmatch(username), 'invalid username'

        # 检查密码是否与确认密码相匹配，如果不匹配则抛出异常
        assert password == confirm_password, 'mismatched password and confirm_password'

        # 检查密码是否满足指定的格式，如果不满足则抛出异常
        assert password_pattern.fullmatch(password), 'invalid password'

        # 调用 RegisterForm 表单对象的 get_hash_password 方法，获取哈希密码
        hash_password = form.get_hash_password()

        # 调用 User 模型的 create_user 方法，创建用户并将用户信息存入数据库
        User.create_user(username, hash_password)

        # 注册成功后重定向到登录页面 '/login'
        return redirect('/login')

    except AssertionError as e:
        # 如果注册失败，获取异常消息，并将消息传递给 register.html 模板进行显示
        message = e.args[0] if len(e.args) else str(e)
        return render_template('register.html', form=RegisterForm(), message=message)


