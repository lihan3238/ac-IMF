"""
logout.py 是一个 Flask 蓝图（Blueprint）模块，包含与用户登出（注销）相关的视图函数。
这些视图函数用于处理用户登出的 HTTP 请求，并执行相关的登出操作。
通过装饰器 @logout.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

在登出过程中，首先从请求的 cookies 中获取 token，
然后调用 OnlineUser 模型的 verify_token 方法来验证 token 是否有效。
如果 token 有效，则通过调用 OnlineUser 模型的 delete_record 方法删除对应的在线用户记录，
然后返回登出页面。如果 token 无效，则说明用户未登录或登录已经过期，
将会重定向到登录页面 '/login'。这样确保用户只能登出其自身的在线会话。

"""



# 导入需要的模块和函数
from flask import Blueprint, render_template, redirect, request

# 创建名为 'logout' 的 Flask 蓝图
logout = Blueprint('logout', __name__)

# 定义处理根路由（'/logout'）的视图函数，用于处理用户登出的逻辑
@logout.route('/')
def get__logout():
    # 导入 OnlineUser 模型
    from models import OnlineUser

    # 从请求的 cookies 中获取 token
    token = request.cookies.get('token')

    # 调用 OnlineUser 模型的 verify_token 方法，验证 token 是否有效
    record = OnlineUser.verify_token(token)

    # 如果 token 有效，删除对应的在线用户记录，并返回登出页面
    if record:
        OnlineUser.delete_record(record.id_)
        return render_template('logout.html')
    else:
        # 如果 token 无效，则重定向到登录页面
        return redirect('/login')

