# 使用 Python 中的 nacl 库进行加密和解密操作


from nacl.public import PrivateKey, SealedBox
from nacl.signing import SigningKey
from nacl.secret import SecretBox
from nacl.utils import random
from os.path import exists
from config import nacl_sk_path

# 代码检查一个路径是否存在
# 如果不存在，就生成一个私钥（PrivateKey）并保存到指定的路径中。
# 否则，就读取已存在的私钥

if not exists(nacl_sk_path):
    sk = PrivateKey.generate()
    sk_raw = sk.encode()
    with open(nacl_sk_path, 'wb') as f:
        f.write(sk_raw)
else:
    with open(nacl_sk_path, 'rb') as f:
        sk_raw = f.read()

# 使用 SealedBox 加密传入的明文
def encrypt(plaintext: bytes):
    return SealedBox(PrivateKey(sk_raw).public_key).encrypt(plaintext)

# 使用 SealedBox 解密传入的密文
def decrypt(ciphertext: bytes):
    return SealedBox(PrivateKey(sk_raw)).decrypt(ciphertext)

# 对传入的消息（message）进行签名，并返回签名（signature）
def sign(message: bytes):
    return SigningKey(sk_raw).sign(message).signature

# 用公钥（verify_key）验证传入的消息（message）和签名（signature）是否匹配
def verify(message: bytes, signature: bytes):
    return SigningKey(sk_raw).verify_key.verify(message, signature)

# 生成一个新的对称密钥（symmetric_key）
def new_symmetric_key():
    return random(SecretBox.KEY_SIZE)

# 使用生成的对称密钥对传入的明文进行加密
def symmetric_encrypt(symmetric_key: bytes, plaintext: bytes):
    return SecretBox(symmetric_key).encrypt(plaintext)

# 使用生成的对称密钥对传入的密文进行解密
def symmetric_decrypt(symmetric_key: bytes, ciphertext: bytes):
    return SecretBox(symmetric_key).decrypt(ciphertext)

# 返回私钥的公钥编码
def get_pk_raw():
    return PrivateKey(sk_raw).public_key.encode()

# 生成一个新的密钥对，包括私钥（sk）和公钥（public_key）的编码
def new_pair():
    sk = PrivateKey.generate()
    return sk.encode(), sk.public_key.encode()
