import hashlib


def md5(value: int) -> str:
    r = hashlib.md5(str(value).encode())
    return r.hexdigest()


def sha256(value: int) -> str:
    r = hashlib.sha256(str(value).encode())
    return r.hexdigest()