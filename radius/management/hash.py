
"""Functions for creating MD5 hashes for FreeRadius"""

import hashlib
import base64
from os import urandom


def smd5(key, salt):
    """Create a salted MD5 hash

    Parameters
    ----------
    key : bytes
        Byte array key (password) to hash
    salt : bytes
        Salt to append to the key before hashing. Should be generated
        securely and randomly.

    Returns
    -------
    str
        Computed hash, with the salt appended::
            +-----------------+------+
            | hash (32 bytes) | salt |
            +-----------------+------+
    """

    md5 = hashlib.md5()

    md5.update(key)
    md5.update(salt)

    return md5.digest() + salt


def make_md5(key, length):
    """Create a salted MD5 hash according to freeradius' specifications.

    Parameters
    ----------
    key : str
        Key to hash
    length : int
        Length of salt
        (generated with ``secrets.token_bytes`` or ``os.urandom``)

    Returns
    -------
    str
        First, the salt is appended to the key and hashed; then, the raw salt
        is appended to the hash. Finally, the byte array (32 bytes + salt) is
        encoded as a base64 string.
    """

    return base64.b64encode(
        smd5(
            key.encode("utf-8"),
            urandom(length))).decode("utf-8")


if __name__ == "__main__":

    import sys
    key = sys.argv[1]

    print(("Creating hash for key {key}:").format(key=key))
    print(make_md5(key, 16))
