"""
这段代码实现了用户的注册功能，将用户的信息和加密后的密钥存储到数据库中
同时提供了查询功能，可以根据条件查找用户记录。
在用户注册过程中，使用了自定义的 secret 模块执行加密操作，保护用户的敏感信息。

get_by(cls, **kwargs)实现查询操作，用于创建用户
create_user(cls, username, hash_password)实现了用户的创建
"""


from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from database import db


# 定义了一个名为 user 的数据库模型类
# 该类继承自 db.Model，表明它是一个 SQLAlchemy 的数据库模型。

class User(db.Model):

    # 定义了表名为 users
    # 定义了七个参数

    # 第一个参数为 id
    # 第二个参数为 create_time，表示创建时间。
    # 第三个参数为 username，记录用户名字。
    # 第四个参数为 hash_password，用于存储用户的密码的哈希值
    # 第五个参数为 encrypted_symmetric_key
    # 用于记录加密后的对称密钥。
    # 第六个参数为加密后的私钥。
    # 第七个参数位加密后的公钥。

    __tablename__ = 'users'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, default=func.now())
    username = Column(String(64), unique=True)
    hash_password = Column(LargeBinary(64))
    encrypted_symmetric_key = Column(LargeBinary(32), nullable=False)
    encrypted_private_key = Column(LargeBinary(32), nullable=False)
    encrypted_public_key = Column(LargeBinary(32), nullable=False)


    # 用于根据指定的条件查询数据库中的记录

    @classmethod
    def get_by(cls, **kwargs):
        #数据库查询操作。
        return cls.query.filter_by(**kwargs).first()



    # 用于创建新的用户记录并将其存储到数据库中。

    @classmethod

    # username 和 hash_password 是必需的参数
    # 用于创建新用户的用户名和经过哈希处理的密码。
    def create_user(cls, username, hash_password):

        # 导入自定义的 secret 模块
        # 该模块用于执行加密操作。
        import secret
        
        # 查询是否已经存在具有相同用户名的用户记录。
        user = User.get_by(username=username)

        # 检查变量 user 是否为空
        # 若不为空，抛出 AssertionError 并显示消息
        # 表示该用户名已经被注册，不允许重复注册。
        assert user is None, 'email already registered'

        # 随机生成一个用户的对称密钥与公私钥

        # 调用 secret 模块中的
        # new_symmetric_key() 方法随机生成一个用户的对称密钥。
        symmetric_key = secret.new_symmetric_key()

        # 调用 secret 模块中的
        # new_pair()方法随机生成一对公私钥。
        private_key, public_key = secret.new_pair()

        # 再用服务器的公钥加密这些密钥，并存储
        user = User(username=username, hash_password=hash_password,
                    encrypted_symmetric_key=secret.encrypt(symmetric_key),
                    encrypted_private_key=secret.encrypt(private_key),
                    encrypted_public_key=secret.encrypt(public_key)
                    )
        
        # 将新创建的用户记录添加到数据库会话中。
        db.session.add(user)

        # 提交数据库会话，将新用户记录保存到数据库中。
        db.session.commit()
