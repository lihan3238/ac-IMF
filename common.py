# 用于设置Cookie的辅助函数
# token是Cookie值的令牌(Token)字符串
def set_token(html: str, token: str):
    # 函数从flask库中导入make_response函数。这个函数用于创建一个Flask的响应对象。
    from flask import make_response
    # 使用make_response函数以html为参数创建一个响应对象r。
    r = make_response(html)
    # 响应对象的set_cookie方法，将token设置为名为"token"的Cookie值
    r.set_cookie('token', token)
    return r


# 自定义的打印函数，它用于将输出内容打印到标准错误流（stderr）
def eprint(*args, **kwargs):
    # 函数从sys模块中导入stderr对象，它表示标准错误流。
    from sys import stderr
    # 通过kwargs['file'] = stderr将标准错误流赋值给关键字参数字典中的"file"键，这样后续的print函数会将输出内容发送到标准错误流。
    kwargs['file'] = stderr
   
    # 函数调用内置的print(*args, **kwargs)函数，将收到的位置参数和关键字参数原封不动地传递给print函数，实现将内容输出到标准错误流的目的。
    # 使用print函数来输出调试信息、错误信息或其他提示信息到控制台，便于调试和查看程序的运行状态
    return print(*args, **kwargs)

# 这是一个装饰器函数login_required，它用于要求用户在访问某些页面或执行某些操作之前必须登录。
def login_required(func):
    # 装饰器从flask模块中导入request对象和redirect函数。request对象用于获取请求信息，redirect函数用于重定向到其他页面。
    from flask import request, redirect
    # 从functools模块中导入wraps装饰器，这是为了保留被装饰函数的元数据信息，避免在装饰后丢失原始函数的属性。
    from functools import wraps
    # 从models模块中导入User类，假设这是一个用于处理用户信息的模型类
    from models import User

    @wraps(func)
    def wrapper(*args, **kwargs):
        from models import OnlineUser
        # 从请求中获取名为"token"的Cookie
        token = request.cookies.get('token')
        # 使用OnlineUser.verify_token(token)来验证该令牌的有效性。
        record = OnlineUser.verify_token(token)
        if record:
            # 如果验证通过（令牌有效），则使用OnlineUser.create_record创建一个新的Token，并将用户的ID存储在数据库中。这可能是用于更新用户会话状态的逻辑。
            token = OnlineUser.create_record(record.id_)
            # 如果存在"user"参数，我们从数据库中查询User模型获取对应的用户对象，并将其作为关键字参数传递给装饰的函数。
            if 'user' in func.__code__.co_varnames:
                kwargs['user'] = User.get_by(id_=record.id_)
                # 如果用户的Token验证通过，我们调用装饰的函数func(*args, **kwargs)，并将得到的结果作为响应。
            return set_token(func(*args, **kwargs), token)
        else:
            # 如果用户的Token验证未通过，我们使用redirect('/login')将用户重定向到登录页面。
            return redirect('/login')
    return wrapper
