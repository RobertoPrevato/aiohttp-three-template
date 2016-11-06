#
# Crypto.Cipher AES wrapper that supports variable length strings when using CBC mode.
# https://pypi.python.org/pypi/pycrypto
#
import base64
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AesEncryptor:

    @staticmethod
    def try_decrypt(text, encryption_key):
        try:
            decrypted = AesEncryptor.decrypt(text, encryption_key)
            if not decrypted:
                return False, decrypted
            return True, decrypted
        except Exception:
            pass
        return False, None

    @staticmethod
    def encrypt(text, encryption_key):
        text = pad(text)
        encryption_key = AesEncryptor.normalize_key(encryption_key)
        iv = Random.new().read(BS)
        aes = AES.new(encryption_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + aes.encrypt(text))

    @staticmethod
    def decrypt(encrypted, encryption_key):
        # normalize key
        encryption_key = AesEncryptor.normalize_key(encryption_key)
        encrypted = base64.b64decode(encrypted)
        iv = encrypted[:16]
        aes = AES.new(encryption_key, AES.MODE_CBC, iv)
        dec = aes.decrypt(encrypted[16:])
        return unpad(dec).decode("utf-8")

    @staticmethod
    def normalize_key(encryption_key):
        if len(encryption_key) >= 32:
            return encryption_key[:32]
        return pad(encryption_key)

