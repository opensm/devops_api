from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from utils.exceptions import CryptoDecodeException, CryptoEncodeException
from devops_api.settings import SECRET_KEY
from base64 import b64decode


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


generator = GenerateCrypto()
secret_data = generator.generate_secret
__all__ = [
    'secret_data',
    'generator'
]
