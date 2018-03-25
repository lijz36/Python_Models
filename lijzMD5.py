import hashlib
from uuid import uuid4


# 加密用户密码工具函数
def md5_hash(pwd):
    digest = hashlib.md5()
    digest.update(pwd.encode('utf-8'))
    return digest.hexdigest()


# 加密用户session工具函数
def md5_uuid():
    m = hashlib.md5()
    m.update(uuid4().bytes)
    return m.hexdigest()