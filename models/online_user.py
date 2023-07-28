"""
函数 new_available_token(cls)，用于创建新令牌，令牌令牌通常用于进行身份验证或会话管理。
在这个具体的代码中，令牌用于管理在线用户。

函数 create_record(cls, id_)，用于创建在线用户记录

函数 delete_record(cls, id_)，用于删除在线用户记录

函数 get_by(cls, **kwargs)，用于根据指定条件查询在线用户记录。
它接收一个可变数量的关键字参数 kwargs，用于指定查询条件。
 
函数 verify_token(cls, token) 用于验证令牌是否有效,config中规定了一个期限
根据上面函数查询出的在线用户记录 用现在的时间减去上次登陆时间，
若大于期限，则判断用户长时间未登陆则表示令牌无效
"""


from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import TIMESTAMP
#从自定义的 database 模块中导入了 db 对象
#该对象是 SQLAlchemy 的数据库对象，用于与数据库进行交互。
from database import db
from common import *


#定义了一个名为 OnlineUser 的数据库模型类
# 该类继承自 db.Model，表明它是一个 SQLAlchemy 的数据库模型。
class OnlineUser(db.Model):

    # 定义表名字为 online_users
    # 定义了三个参数
    # 第一个为 id,关联到 users 表的 id_ 列,自增
    # 第二个为 token，存储用户的唯一对应令牌
    # 第三个为 last_used,用于记录用户最后一次使用的时间。

    __tablename__ = 'online_users'
    id_ = Column(Integer, ForeignKey('users.id_'), primary_key=True, autoincrement=True)
    token = Column(String(32), primary_key=True)
    last_used = Column(TIMESTAMP)

    @classmethod

    # 用于生成一个新的可用令牌（token）。
    # 并从数据库中获取所有记录，并将 token 存储在列表中。
    # 然后，生成新的 token
    # 并检查是否与数据库中已有的 token 冲突
    # 如果没有冲突，则返回这个新的 token。

    def new_available_token(cls):

        # uuid4 用于生成一个随机的 UUID.
        from uuid import uuid4

        # 数据库查询，返回 OnlineUser 类中所有的记录
        record_list = cls.query.all()

        # 通过列表推导式，提取所有记录的 token 字段，
        token_list = list(record.token for record in record_list)

        # 生成令牌，与原令牌对比
        # 无限循环，知道找到一个可用的新令牌
        while True:
            token = uuid4().hex
            if token not in token_list:
                record = cls.query.filter(cls.token == token).first()
                if record is None:
                    return token



    # 用于创建在线用户记录，若有记录，则更新，若没有记录，生成新纪录
    @classmethod
    def create_record(cls, id_):

        # 用于获取当前的日期和时间信息。
        from datetime import datetime

        # 生成一个新的可用令牌。
        token = cls.new_available_token()

        # 获取具有指定 id_ 的在线用户记录。
        record = cls.get_by(id_=id_)

        # 检查指定id_的在线用户记录是否存在
        # 如果不存在，说明该用户没有在线记录
        # 则需要创建一个新的 OnlineUser 记录。
        if record is None:
            record = OnlineUser(id_=id_, token=token)

            # 创建一个新的 OnlineUser 记录，
            record.last_used = datetime.now()

            # 将新创建的记录添加到数据库会话中。
            db.session.add(record)

        # 存在在线记录 
        # 更新
        else:
            record.token = token
            record.last_used = datetime.now()

        #提交数据库会话
        db.session.commit()

        #返回生成的令牌 token。
        return token

    @classmethod
    # 用于删除在线用户记录。
    def delete_record(cls, id_):

    # 查询数据库具有指定 id_ 的在线用户记录。
        record = cls.get_by(id_=id_)

        # 检测指定id_的在线用户记录是否存在
        # 如果存在，进行删除操作。
        if record:

            # 将查询到的在线用户记录从数据库会话中删除。
            db.session.delete(record)

            # 提交数据库会话，将删除操作保存到数据库中。
            db.session.commit()

    @classmethod

    # 用于根据指定条件查询在线用户记录
    def get_by(cls, **kwargs):

        # 使用 SQLAlchemy 的查询功能
        # 根据指定条件查询数据库中的在线用户记录。
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    #用于验证令牌是否有效。
    def verify_token(cls, token):

        #用于获取当前的日期和时间信息。
        from datetime import datetime

        #导入 token_expired 变量
        # 该变量是指定令牌的有效期限，以秒为单位。
        from config import token_expired

        # 查询数据库具有指定 token 的在线用户记录。
        record = cls.get_by(token=token)

        # 在线用户记录若存在是否存在，继续
        if record is not None:

            # 获取令牌最后一次使用的时间。
            last_used = record.last_used

            # 获取当前的日期和时间。
            now = datetime.now()

            #计算当前时间与令牌最后使用时间的差值
            delta = now-last_used

            # 将时间间隔对象转换为总秒数
            # 得到两个时间点之间的秒数差。
            total_seconds = delta.total_seconds()

            #将时间差 total_seconds 打印输出。
            eprint(total_seconds)

            #检查时间差是否小于令牌的有效期（以秒为单位）。
            # 若小于有效期，则说明令牌是有效的。
            # 如果令牌有效，返回查询到的在线用户记录。
            # 否则，返回 None，表示令牌无效。

            if total_seconds < token_expired:
                return record
            
        return None
