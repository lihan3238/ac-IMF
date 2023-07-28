"""
file.py 是一个 Flask 蓝图（Blueprint）模块，包含了与文件操作相关的视图函数。
这些视图函数用于处理与文件上传、下载、删除、分享等功能相关的 HTTP 请求，并返回相应的页面或数据。
通过装饰器 @file.route() 将不同的 URL 路径映射到相应的视图函数，
处理对应的 HTTP 请求并返回相应的页面或数据。每个视图函数的功能在代码中都有详细的注释说明。

"""


# 导入需要的模块和函数
from flask import Blueprint, render_template, flash, redirect, request
from models import File
from common import *


# 创建名为 'file' 的 Flask 蓝图
file = Blueprint('file', __name__)

# 定义处理根路由（'/file'）的视图函数，用于展示当前用户上传的文件列表
@file.route('/')
@login_required
def get__file(user):
    # 导入 File 模型
    from models import File

    # 从数据库中查询当前用户上传的所有文件
    files = File.query.filter(File.creator_id == user.id_).all()

    # 渲染 file.html 模板并传递用户名和文件列表
    return render_template('file.html', username=user.username, files=files)

# 定义处理 '/upload' 路由的视图函数，用于展示上传文件的表单
@file.route('/upload')
@login_required
def get__upload():
    # 导入 FileForm 表单类
    from form import FileForm

    # 渲染 file_upload.html 模板并传递表单对象
    return render_template('file_upload.html', form=FileForm())

# 定义处理 '/upload' POST 请求的视图函数，用于处理用户上传文件的逻辑
@file.route('/upload', methods=['POST'])
@login_required
def post__upload(user):
    try:
        # 导入 FileForm 表单类
        from form import FileForm

        # 创建表单对象并验证提交的数据
        form = FileForm()
        #assert form.validate_on_submit(), 'invalid form fields'
        assert form.is_submitted() and form.validate(),'invalid form fields'
        # 获取上传的文件数据
        data = form.file.data

        # 调用 File 模型的 upload_file 方法，将文件上传到数据库
        File.upload_file(user, data)

        # 如果上传成功，显示上传成功的提示信息
        flash('上传成功！')

    except AssertionError as e:
        # 如果上传失败，显示上传失败的提示信息，并将具体错误信息显示在提示中
        message = e.args[0] if len(e.args) else str(e)
        flash('上传失败！' + message)

    # 无论上传成功或失败，都重定向到文件列表页面
    return redirect('/file')

# 定义处理 '/remove' 路由的视图函数，用于处理删除文件的逻辑
@file.route('/remove')
@login_required
def get__remove(user):
    try:
        # 获取请求参数中的文件名
        filename = request.args.get('filename')

        # 检查是否提供了文件名，如果没有则抛出异常
        assert filename, 'missing filename'

        # 调用 File 模型的 delete_file 方法，从数据库中删除文件
        File.delete_file(user, filename)

        # 如果删除成功，显示删除成功的提示信息
        flash('删除成功！')

    except AssertionError as e:
        # 如果删除失败，显示删除失败的提示信息，并将具体错误信息显示在提示中
        message = e.args[0] if len(e.args) else str(e)
        flash('删除失败！' + message)

    # 无论删除成功或失败，都重定向到文件列表页面
    return redirect('/file')

# 定义处理 '/download' 路由的视图函数，用于处理下载文件的逻辑
@file.route('/download')
@login_required
def get__download(user):
    try:
        # 获取请求参数中的文件名
        filename = request.args.get('filename')

        # 检查是否提供了文件名，如果没有则抛出异常
        assert filename, 'missing filename'

        # 获取请求参数中的文件类型
        type_ = request.args.get('type')

        # 检查是否提供了文件类型，如果没有则抛出异常
        assert type_, 'missing type'

        # 检查文件类型是否是合法的类型，如果不是则抛出异常
        assert type_ in ('encrypted', 'plaintext', 'signature', 'hashvalue'), 'unknown type'

        # 调用 File 模型的 download_file 方法，返回下载的文件
        return File.download_file(user, filename, type_)

    except AssertionError as e:
        # 如果下载失败，显示下载失败的提示信息，并将具体错误信息显示在提示中
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)

    # 无论下载成功或失败，都重定向到文件列表页面
    return redirect('/file')

# 定义处理 '/share' 路由的视图函数，用于处理设置文件分享的逻辑
@file.route('/share')
@login_required
def get__share(user):
    try:
        # 获取请求参数中的文件名
        filename = request.args.get('filename')

        # 检查是否提供了文件名，如果没有则抛出异常
        assert filename, 'missing filename'

        # 调用 File 模型的 share_file 方法，设置文件分享
        File.share_file(user, filename)

        # 如果设置成功，显示设置成功的提示信息
        flash('设置成功！')

        # 设置成功后，重定向到文件列表页面
        return redirect('/file')

    except AssertionError as e:
        # 如果设置失败，显示设置失败的提示信息，并将具体错误信息显示在提示中
        message = e.args[0] if len(e.args) else str(e)
        flash('设置失败！' + message)

        # 设置失败后，重定向到文件列表页面
        return redirect('/file')
    
