from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired

# 用于处理密码输入


class PasswordForm(FlaskForm):
    """
    这行代码定义了一个名为 password的字段
    PasswordField 表示它用于输入密码类型的数据。字段的标签（即描述信息）被设置为"password"。
    validators=[DataRequired()]，指定了该字段必须包含数据（不能为空），即必须输入密码。
    """
    password = PasswordField('password', validators=[DataRequired()])

    def get_hash_password(self):
        from hashlib import sha512
        # 首先获取表单字段 password的数据，即用户输入的密码。
        # 将密码编码为字节字符串，使用 SHA-512哈希算法对密码进行哈希处理，并返回哈希后的结果（字节形式）。
        return sha512(self.password.data.encode()).digest()

# RegisterForm类额外添加了 username和confirm_password字段，用于处理注册时的用户名和确认密码的输入。


class RegisterForm(PasswordForm):
    # 这行代码定义了一个名为 username的字段，它是一个字符串输入字段（StringField）。
    # StringField表示它用于输入字符串类型的数据，例如用户名。
    # 通过validators=[DataRequired()]，指定了该字段必须包含数据（不能为空），即必须输入用户名。
    username = StringField('username', validators=[DataRequired()])
    # PasswordField表示它用于输入密码类型的数据，用于确认密码。
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired()])

# PasswordForm，LoginForm表单类获得了输入密码的字段和获取哈希密码的方法
# LoginForm类额外添加了 username字段，用于处理登录时的用户名的输入。


class LoginForm(PasswordForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

# 使用 FileForm表单类，你可以在 Flask应用中创建一个文件上传的表单，让用户上传文件。
# 当用户提交表单时，表单将验证文件上传字段是否包含文件，如果没有上传文件，则会产生验证错误。


class FileForm(FlaskForm):
    from flask_wtf.file import FileRequired
    # 这行代码定义了一个名为 file的字段，它是一个文件上传字段（FileField）。
    # FileField表示它用于处理文件上传类型的数据
    # 字段的标签（即描述信息）被设置为"file"
    file = FileField('file', validators=[FileRequired()])
