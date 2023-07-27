from flask_sqlalchemy import SQLAlchemy
from config import mysql_user, mysql_password, mysql_host, mysql_schema

#  创建一个SQLAlchemy实例，这个实例将被用于管理数据库连接和数据库操作。
db = SQLAlchemy()
# 创建一个基础模型类Base，它继承自db.Model。通过继承它，可以让所有模型类共享相同的数据库配置和功能。    
Base = db.Model

# 这是一个用于创建Flask应用的函数。它接受一个name参数作为应用的名称，并返回一个配置好的Flask应用对象。
def create_app(name):
    from flask import Flask
      # 创建一个Flask应用对象，并使用传入的name作为应用的名称。
    app = Flask(name)
    # 来配置数据库连接。在这个例子中，数据库类型是MySQL，并使用mysql+pymysql作为驱动
    # 根据mysql_user、mysql_password、mysql_host和mysql_schema等配置参数来构建数据库连接字符串。
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(mysql_user, mysql_password, mysql_host,mysql_schema)
    # 这个选项用于设置是否追踪对象的修改并发送信号。默认情况下，Flask-SQLAlchemy会在每个请求结束后检测对象的修改情况
    # 如果设置为True，则会发送信号。这样的信号在大多数情况下是不必要的，并且会产生一些额外的开销
    # 建议设置为False，特别是在大型应用中或性能要求较高的情况下。
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 这个选项用于设置是否在每个请求结束后自动提交数据库的变更。
    # 当设置为True时，在每个请求的末尾，如果没有发生异常，则会自动调用db.session.commit()来提交数据库的变更
    # 如果设置为False，则需要手动调用db.session.commit()来提交变更。
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # 使用db.init_app(app)初始化数据库连接，将db对象和Flask应用关联起来。
    db.init_app(app)
    # 这是一个应用上下文管理器。通过app.app_context()可以进入应用上下文环境。
    with app.app_context():
        from models import User
        # 在应用上下文中，调用db.create_all()来创建数据库表。
        db.create_all()
    return app
