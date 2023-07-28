# 用于设置 Cookie的辅助函数
# token是 Cookie值的令牌(Token)字符串
def set_token(html: str, token: str):
    # 函数从 flask 库中导入 make_response 函数。这个函数用于创建一个 Flask的响应对象。
    from flask import make_response
    # 使用 make_response函数以 html为参数创建一个响应对象 r。
    r = make_response(html)
    # 响应对象的 set_cookie方法，将 token 设置为名为"token"的 Cookie 值
    r.set_cookie('token', token)
    return r


# 自定义的打印函数，它用于将输出内容打印到标准错误流（stderr）
def eprint(*args, **kwargs):
    # 函数从 sys 模块中导入 stderr 对象，它表示标准错误流。
    from sys import stderr
    """
    将标准错误流赋值给关键字参数字典中的"file"键，后续 print函数会将输出内容发送到标准错误流。
    函数调用内置的 print(*args, **kwargs)函数，
    将收到的位置参数和关键字参数原封不动地传递给 print函数，实现将内容输出到标准错误流的目的。
    使用 print函数来输出调试信息、错误信息或其他提示信息到控制台，
    便于调试和查看程序的运行状态
    """
    kwargs['file'] = stderr
    return print(*args, **kwargs)

# 这是一个装饰器函数 login_required，它用于要求用户在访问某些页面或执行某些操作之前必须登录。


def login_required(func):
    # 装饰器从 flask模块中导入 request对象和 redirect函数。
    # request对象用于获取请求信息，redirect函数用于重定向到其他页面。
    from flask import request, redirect
    # 从 functools模块中导入 wraps装饰器，保留被装饰函数的元数据信息，避免装饰后丢失原始函数的属性。
    from functools import wraps
    # 从 models模块中导入 User类，假设这是一个用于处理用户信息的模型类
    from models import User

    @wraps(func)
    def wrapper(*args, **kwargs):
        from models import OnlineUser
        # 从请求中获取名为"token"的 Cookie
        token = request.cookies.get('token')
        # 使用 OnlineUser.verify_token(token)来验证该令牌的有效性。
        record = OnlineUser.verify_token(token)
        if record:
            # 如果验证通过（令牌有效），则使用 OnlineUser.create_record 创建一个新的 Token，
            # 并将用户的ID存储在数据库中。这可能是用于更新用户会话状态的逻辑。
            token = OnlineUser.create_record(record.id_)
            # 如果存在"user"参数，我们从数据库中查询User模型获取对应的用户对象，
            # 并将其作为关键字参数传递给装饰的函数。
            if 'user' in func.__code__.co_varnames:
                kwargs['user'] = User.get_by(id_=record.id_)
                # 若 Token验证通过，调用装饰的函数 func(*args, **kwargs)，将得到的结果作为响应。
            return set_token(func(*args, **kwargs), token)
        else:
            # 如果用户的 Token验证未通过，我们使用 redirect('/login')将用户重定向到登录页面。
            return redirect('/login')
    return wrapper
