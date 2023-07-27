"""
这个文件（__init__.py）是一个包含视图函数的模块文件。
在一个 Python 包中，views 目录通常用于存放与应用程序视图相关的代码，
例如处理路由和请求的视图函数。这个文件导入了其他模块中的视图函数，
并将其暴露在当前模块中，使得在其他地方可以通过这个模块访问这些视图函数。
"""

# 从模块中导入具体的视图函数
from .register import register
from .root import root
from .login import login
from .logout import logout
from .file import file
from .shared_file import shared_file

