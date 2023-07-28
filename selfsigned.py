# 生成一个 RSA 密钥对和相应的证书，证书包含主机名、公共 IP 和私有 IP 地址。


def generate_selfsigned_cert(hostname, public_ip, private_ip):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from datetime import datetime, timedelta

    # 生成密钥
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # 创建一个 x509.Name 对象，用于设置证书的主题名称
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, hostname)
    ])
    
    # 创建一个 x509.SubjectAlternativeName 对象，用于设置证书的备用名称（包括主机名、公共 IP 和私有 IP 地址）
    alt_names = x509.SubjectAlternativeName([
        x509.DNSName(hostname),
        x509.IPAddress(public_ip),
        x509.IPAddress(private_ip),
    ])
    
    
    # 创建一个 x509.BasicConstraints 对象，设置证书的基本约束，将其标记为 CA 证书（用于签署其他证书）
    # path_len=0 表示此证书只能对自身进行签名，而不能对其他证书进行签名。
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    
    
    # 创建一个 x509.CertificateBuilder 对象，用于构建证书
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1000)
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=10*365))
        .add_extension(basic_contraints, False)
        .add_extension(alt_names, False)
        .sign(key, hashes.SHA256(), default_backend())
    )

    # 使用以下代码将证书和私钥转换为 PEM 格式
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem
