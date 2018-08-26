
"""Functions for modifying user info in the FreeRadius database"""

from django.conf import settings

from .models import Radcheck
from .hash import make_md5


def add_user(username, password):
    """Add a user account.

    Parameters
    ----------
    username : str
        Target username
    password : str
        Target password
    """

    (
        Radcheck(
            username=username,
            attribute="SMD5-Password",
            op=":=",
            value=make_md5(password, settings.SALT_LENGTH))
        .using("radius")
        .save()
    )
