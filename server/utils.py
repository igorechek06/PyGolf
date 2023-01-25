import hashlib


def hash(password: str, salt: str) -> str:
    return hashlib.sha512(str.encode(password + salt, "UTF-8")).hexdigest()
