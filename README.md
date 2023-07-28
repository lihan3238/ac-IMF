# 中传放心传

本项目基于[中国传媒大学密码学应用实践课程](https://github.com/c4pr1c3/ac)，将半成品完成为完整工程。

## 功能清单

* 基于网页的用户注册与登录系统
  * 使用https绑定证书到域名而非IP地址 【 PKI X.509 】
  * 允许用户注册到系统
    * 用户名的合法字符集范围：中文、英文字母、数字
        * 类似：-、_、.等合法字符集范围之外的字符不允许使用
    * 用户口令长度限制在36个字符之内
    * 对用户输入的口令进行强度校验，禁止使用弱口令
  * 使用合法用户名和口令登录系统
  * 禁止使用明文存储用户口令(SHA512)
    * 存储的口令即使被公开，也无法还原/解码出原始明文口令
* 基于网页的文件上传加密与数字签名系统
  * 已完成《基于网页的用户注册与登录系统》所有要求
  * 限制文件大小：&lt; 10MB（可通过代码配置）
  * 限制文件类型：office文档、常见图片类型
  * 匿名用户禁止上传文件
  * 对文件进行对称加密存储到文件系统，禁止明文存储文件 
  * 文件秒传：服务器上已有的文件，客户端禁止重复上传
  * 用户可以删除自己上传的文件
* 基于网页的加密文件下载与解密
  * 已完成《基于网页的文件上传加密与数字签名系统》所有要求
  * 提供匿名用户加密后文件和关联的数字签名文件的下载
    * 客户端对下载后的文件进行数字签名验证 【 非对称（公钥）加密 数字签名 】
    * 客户端对下载后的文件可以解密还原到原始文件 【 对称解密 密钥管理 】
  * 提供已登录用户解密后文件下载
  * 下载URL设置有效期（限制时间或限制下载次数），过期后禁止访问 【 数字签名 消息认证码 Hash Extension Length Attack Hash算法与HMAC算法的区别与联系 】
  * 提供静态文件的散列值下载，供下载文件完成后本地校验文件完整性 【 散列算法 】

样例工程完成的功能和实际小学期要求完成的大作业功能有一些差异，具体请查看[课程教学Wiki](https://c4pr1c3.github.io/cuc-wiki/ac/2019/index.html#_5)。

同学们可以参考这个样例工程中的代码，自行修改或采用其中的代码片段以完成尽可能多的作业要求。

## 本项目用到的关键技术

* 前端使用flask搭建
* 后端使用Python编写；
* 程序部署运行环境采用 pipenv虚拟环境，pipfile中有项目依赖的包及版本；

## 快速上手体验

### 配置环境(win11+windows powershell)

```
git clone git@github.com:lihan3238/ac-IMF.git
pipenv shell
pipenv install
```
### 连接数据库

```config.py
- config.py中填写数据库用户、密码、host，新建空白数据库后，填写数据库名称
# MySQL
# database.py
mysql_user = 'cuc_cloud'
mysql_password = ''
mysql_host = '127.0.0.1'
mysql_schema = 'cuc_cloud_database'
```

### 部署服务器

```
python gen_selfsigned.py
python run.py
```
打开浏览器访问： [https://cloudpan.cuc.edu.cn:80/login/](https://cloudpan.cuc.edu.cn:80/login/) 即可快速体验系统所有功能。

## 依赖环境安装补充说明

* 如果本机没有pipenv，则需先安装pipenv
```
pip install pipenv
```
* 注意要给数据库用户操作数据库的权限

## 演示

[![查看演示视频]()]()

## 附录-1：项目测试验证环境信息

```
Server:

Pipfile:
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
cryptography = "*"
flask-wtf = "*"
wtforms = "==2.2.1"
sqlalchemy = "==1.4.0"
pynacl = "*"
flask-sqlalchemy = "*"
pymysql = "==0.9.1"
update = "*"
jinja2 = "==2.11.3"
markupsafe = "==2.0.1"
pyotp = "*"

[dev-packages]

[requires]
python_version = "3.10"

[pipenv]
allow_prereleases = true
```
