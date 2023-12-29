from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.PublicKey import RSA
from Crypto import Random
from utils.exceptions import CryptoDecodeException, CryptoEncodeException
from devops_api.settings import SECRET_KEY
from base64 import b64decode
import base64
import hashlib


class GenerateCrypto:
    salt = None
    private_key = None
    public_key = None

    @property
    def generate_secret(self):
        if self.salt:
            random_generator = "{}{}".format(self.salt, Random.new().read)
        else:
            random_generator = Random.new().read
        try:
            rsa = RSA.generate(1024, random_generator)
            self.private_key = rsa.export_key()
            public_key = rsa.public_key()
            return self.private_key.decode(), public_key.export_key().decode()
        except CryptoEncodeException:
            raise CryptoEncodeException()

    def decrypt_data(self, data):
        try:
            # dsize = SHA.digest_size
            sentinel = Random.new().read(1024 + 1024)
            private_key = RSA.import_key(self.private_key)
            cipher_rsa = PKCS1_v1_5.new(private_key)
            return cipher_rsa.decrypt(b64decode(data), sentinel)
        except CryptoDecodeException:
            raise CryptoDecodeException()


class AESCipher(object):

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pack_data(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpack_data(cipher.decrypt(enc[AES.block_size:]))

    @staticmethod
    def _pack_data(s):
        return s + ((AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)).encode(
            'utf-8'
        )

    @staticmethod
    def _unpack_data(s):
        data = s[:-ord(s[len(s) - 1:])]
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return data


generator = GenerateCrypto()
secret_data = generator.generate_secret
__all__ = [
    'secret_data',
    'generator',
    'AESCipher'
]
