"""
此文件定义了 File 类, 包含:
表 files 的定义
上传文件方法 upload_file
删除文件方法 delete_file
下载文件方法 download_file
分享文件方法 share_file
"""


from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_
from os import remove, path, mkdir
import re
from database import db
from config import storage_path
import secret

# 使用正则表达式检查文件名中是否包含非中文字符
filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    """
    定义表 files
    字段有:文件的创建者ID、文件名、哈希值和共享状态，
    并通过外键约束与 users 表中的用户记录关联。
    文件名和创建者ID共同作为主键，保证每个文件记录的唯一性。
    """
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey(
        'users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))
    shared = Column(Boolean, default=False)

    """
    定义了类方法 upload_file，用于上传文件。该方法首先对文件名进行校验，然后检查文件类型是否合法。
    接着，读取文件内容，对其进行大小限制，然后计算文件内容的哈希值。
    如果文件不存在，将对文件内容进行加密，并将加密后的内容和签名保存到指定的存储路径。
    最后，将文件信息添加到数据库中。
    """
    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha512
        from config import allowed_file_suffix_list
        filename = data.filename

        # 校验文件名长度不超过64个字符
        assert len(filename) <= 64, 'filename too long (>64B)'

        # 校验文件名中不包含非中文字符
        assert filename_pattern.fullmatch(
            filename), 'no unicode character allowed'

        # 获取文件名后缀
        filename_suffix = filename.rsplit('.', maxsplit=1)[-1]

        # 校验文件后缀是否在允许的文件类型列表中
        assert filename_suffix in allowed_file_suffix_list, 'banned file type'

        # 查询数据库，判断文件是否已存在
        f = File.query.filter(
            and_(File.creator_id == user.id_, File.filename == filename)).first()

        # 断言文件不存在，避免重复上传同名文件
        assert not f, 'file already exists'

        # 读取上传的内容,并检查是否小于10MB
        content = data.read()
        assert len(content) < 1*1024*1024, 'file too large (>=10MB)'

        # 构建用户的文件存储路径
        user_id = str(user.id_)+'/'

        # 如果用户的存储路径不存在，则创建目录
        if not path.exists(storage_path+user_id):
            if not path.exists(storage_path):
                mkdir(storage_path)
            mkdir(storage_path+user_id)

        # 计算原文件的哈希
        hash_value = sha512(content).hexdigest()

        # 判断文件是否存在
        if not path.exists(storage_path+user_id+hash_value):
            # 加密并存储。加密前得先还原出对称密钥。
            content = secret.symmetric_encrypt(
                secret.decrypt(user.encrypted_symmetric_key), content)
            # 同时计算签名
            signature = secret.sign(content)
            # 保存密文与签名
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
            with open(storage_path+user_id+hash_value+'.sig', 'wb') as f:
                f.write(signature)

        # 用户ID作为文件的创建者ID
        creator_id = user.id_

        # 创建文件记录，并将其添加到数据库中
        file = File(creator_id=creator_id,
                    filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()

    """
    定义了类方法 delete_file，用于删除文件
    根据用户和文件名查找对应的文件记录，然后从数据库中删除该记录，并删除对应的文件和签名。
    """
    @classmethod
    def delete_file(cls, user, filename):
        # 查询数据库，获取文件记录
        f = File.query.filter(
            and_(File.creator_id == user.id_, File.filename == filename)).first()

        # 断言文件记录存在，若不存在则抛出异常，提示找不到该文件
        assert f, 'no such file ({})'.format(filename)

        # 获取文件的哈希值
        hash_value = f.hash_value

        # 删除文件记录，并将更改提交到数据库
        db.session.delete(f)
        db.session.commit()

        
        files = File.query.filter(File.hash_value == hash_value).all()

        
        if not len(files):
            remove(storage_path+str(user.id_)+'/'+hash_value)
            remove(storage_path+str(user.id_)+'/'+hash_value+'.sig')

    """
    download_file方法,根据用户和文件名查找对应的文件记录,
    然后根据下载类型（哈希值、签名、明文或加密文件）读取相应的内容，并构造响应以便下载
    """
    @classmethod
    def download_file(cls, user, filename, type_):
        from flask import make_response
        # 查询数据库，获取文件记录
        f = File.query.filter(
            and_(File.creator_id == user.id_, File.filename == filename)).first()

        # 断言文件记录存在，若不存在则抛出异常，提示找不到该文件
        assert f, 'no such file ({})'.format(filename)

        # 获取文件的哈希值
        hash_value = f.hash_value

        # 根据下载类型进行不同处理
        if type_ == 'hashvalue':
            content = hash_value
            filename = filename + '.hash'
        elif type_ == 'signature':
            # 读取签名
            with open(storage_path+str(user.id_)+'/'+hash_value+'.sig', 'rb') as f_:
                content = f_.read()
                filename = filename+'.sig'
        else:
            # 读取密文
            with open(storage_path+str(user.id_)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            if type_ == 'plaintext':
                content = secret.symmetric_decrypt(
                    secret.decrypt(user.encrypted_symmetric_key), content)
            elif type_ == 'encrypted':
                filename = filename + '.encrypted'

        # 创建下载响应
        response = make_response(content)

        # 设置响应头部，指定下载文件的文件名
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)

        return response

    @classmethod
    def share_file(cls, user, filename):
        # 查询数据库，获取文件记录
        f = File.query.filter(
            and_(File.creator_id == user.id_, File.filename == filename)).first()
        
        # 断言文件记录存在，若不存在则抛出异常，提示找不到该文件
        assert f, 'no such file ({})'.format(filename)
        # 切换文件的共享状态，将 shared 属性取反
        f.shared = not f.shared
        # 提交更改到数据库
        db.session.commit()
