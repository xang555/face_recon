from os import urandom
from hashlib import sha256
import hmac
from base64 import b64encode

# my hash password
def hashPassword(password= None):
    """
    use for hash password for this application
    :param password: str
    :return: str
    """
    if password is None and not isinstance(password, str):
        return None

    salt = "55765567"
    raw_pass = salt + password
    hash_passwd = sha256(raw_pass.encode('utf-8')).digest()

    return b64encode(hash_passwd).decode('utf-8')
