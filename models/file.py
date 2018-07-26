from sqlalchemy import Column, String, Integer, ForeignKey, and_
from os import remove, path, mkdir
from database import db
from config import storage_path


class File(db.Model):
    __tablename__ = 'files'
    creator_id = Column(Integer, ForeignKey('users.id_', ondelete='CASCADE'), primary_key=True, autoincrement=True)
    filename = Column(String(64), primary_key=True)
    hash_value = Column(String(128))

    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha512
        from config import allowed_file_suffix_list
        filename = data.filename
        assert len(filename) <= 64, 'filename too long (>64B)'
        filename_suffix = filename.rsplit('.', maxsplit=1)[-1]
        assert filename_suffix in allowed_file_suffix_list, 'banned file type'
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert not f, 'file already exists'
        content = data.read()
        assert len(content) < 1*1024*1024, 'file too large (>=10MB)'
        creator_id = user.id_
        hash_value = sha512(content).hexdigest()
        user_id = str(user.id_)+'/'
        if not path.exists(storage_path+user_id):
            mkdir(storage_path+user_id)
        if not path.exists(storage_path+user_id+hash_value):
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
        file = File(creator_id=creator_id, filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()

    @classmethod
    def delete_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id_, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        db.session.delete(f)
        db.session.commit()
        files = File.query.filter(File.hash_value == hash_value).all()
        if not len(files):
            remove(storage_path+str(user.id_)+'/'+hash_value)