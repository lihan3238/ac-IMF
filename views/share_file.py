"""
shared_file.py 是一个 Flask 蓝图（Blueprint）模块，包含与共享文件相关的视图函数。
这些视图函数用于处理对共享文件的 HTTP 请求，并返回相应的页面或数据。
通过装饰器 @shared_file.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

get__ 视图函数用于显示共享的文件列表。它查询所有已共享的文件，并查询每个文件的创建者用户名。
然后，将文件名和对应的创建者用户名组合成一个列表，传递给 shared_file.html 模板进行渲染。

get__download 视图函数用于下载共享文件。它从请求参数中获取文件名、用户名和类型，
然后根据用户名查询用户对象，并调用 File 模型的 download_file 方法来下载共享文件。
如果下载失败，则在页面上显示相应的错误提示信息，并重定向到共享文件列表页面。

"""



# 导入需要的模块和函数
from flask import Blueprint, render_template, request, flash, redirect

# 创建名为 'shared_file' 的 Flask 蓝图
share_file = Blueprint('share_file', __name__)

# 定义处理根路径（'/shared_file'）的视图函数，用于显示共享的文件列表
@share_file.route('/')
def get__():
    # 导入 File 和 User 模型
    from models import File, User

    # 从数据库中查询所有已共享的文件
    files = File.query.filter(File.shared).all()

    # 查询每个文件的创建者（用户），并将其存储在 users 列表中
    users = list(User.get_by(id_=file.creator_id) for file in files)

    # 将文件名和对应的创建者用户名组合成一个列表，存储在 list_ 中
    list_ = list((file.filename, user.username) for file, user in zip(files, users))

    # 渲染 shared_file.html 模板，并传递 list_ 列表作为参数
    return render_template('share_file.html', list=list_)

# 定义处理 '/download' 路由的视图函数，用于下载共享文件
@share_file.route('/download')
def get__download():
    # 导入 User 和 File 模型
    from models import User, File

    try:
        # 从请求参数中获取文件名、用户名和类型
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        username = request.args.get('username')
        assert username, 'missing username'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'signature'), 'unknown type'

        # 根据用户名查询用户对象
        user = User.get_by(username=username)

        # 调用 File 模型的 download_file 方法，下载共享文件
        return File.download_file(user, filename, type_)

    except AssertionError as e:
        # 如果下载失败，获取异常消息，并将消息传递给 flash 进行显示
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)

        # 下载失败后重定向到共享文件列表页面
        return redirect('/share_file')

