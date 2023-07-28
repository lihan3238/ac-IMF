from selfsigned import generate_selfsigned_cert
from ipaddress import IPv4Address



if __name__ == '__main__':
    # 定义 hostname, public_ip, private_ip: 这些变量分别用于设置要生成证书的主机名，公共 IP地址和私有IP地址。
    hostname = 'cloudpan.cuc.edu.cn'
    public_ip, private_ip = [IPv4Address('127.0.0.1')]*2

    # 调用 generate_selfsigned_cert(hostname, public_ip, private_ip)来生成自签名 SSL证书和私钥。
    # 这个函数返回一个包含证书和私钥内容的元组。
    cert_pem, key_pem = generate_selfsigned_cert(hostname, public_ip, private_ip)


    # 遍历 files.items()，即遍历 files字典中的键值对。对于每个文件名和内容，打开文件并写入相应的内容。
    # 这样就将生成的证书和私钥保存到了文件中。
    files = {'cert.pem': cert_pem, 'key.pem': key_pem}
    for filename, content in files.items():
        # 这是一个文件操作的上下文管理器。使用 open()函数打开文件，filename是文件名
        # 'wb'表示以二进制写入模式打开文件，即以二进制方式写入内容。
        # with语句可以确保在代码块执行完后，文件会被正确关闭，不需要显式调用 f.close()。
        with open(filename, 'wb') as f:
            # 使用 f.write()方法将 content写入文件。
            f.write(content)
