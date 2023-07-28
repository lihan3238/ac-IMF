"""
root.py 是一个 Flask 蓝图（Blueprint）模块，包含与根路径和公钥获取相关的视图函数。
这些视图函数用于处理对根路径和公钥的 HTTP 请求，并返回相应的页面或数据。
通过装饰器 @root.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

index 视图函数用于显示主页 index.html，
使用了 @login_required 装饰器来确保用户在登录状态下才能访问主页。

public_key 视图函数用于获取公钥并提供下载。
它调用 secret 模块的 get_pk_raw 函数来获取公钥的原始数据，
并通过 make_response 创建一个带有公钥数据的响应对象。
然后，设置响应头的 Content-Disposition，指定文件名为 public_key，以便客户端进行公钥的下载。
"""


# 导入需要的模块和函数
from flask import Blueprint, render_template, make_response
from common import *

# 创建名为 'root' 的 Flask 蓝图
root = Blueprint('root', __name__)

# 定义处理根路径（'/'）的视图函数，用于显示主页


@root.route('')
@login_required
def index():
    # 渲染 index.html 模板
    return render_template('index.html')

# 定义处理 '/public_key' 路由的视图函数，用于获取公钥并提供下载


@root.route('public_key')
def public_key():
    # 导入 secret 模块，用于获取公钥原始数据
    from secret import get_pk_raw

    # 调用 get_pk_raw 函数，获取公钥原始数据
    response = make_response(get_pk_raw())

    # 设置响应头的 Content-Disposition，指定文件名为 'public_key'，以便客户端下载
    response.headers['Content-Disposition'] = 'attachment; filename=public_key'

    # 返回带有公钥数据的响应对象
    return response
