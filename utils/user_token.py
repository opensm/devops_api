from devops_api.settings import SECRET_KEY
import time
import hashlib


def make_token(username):
    """
    :param username:
    :return:
    """
    md5 = hashlib.md5(
        "{0}{1}{2}".format(username, time.time(), SECRET_KEY).encode("utf8")
    )
    return md5.hexdigest()
