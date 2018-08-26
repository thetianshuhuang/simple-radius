
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

    Returns
    -------
    bool
        True if successful, False otherwise
    str
        Explanation of error.
    """

    # Check if username already exists
    if (len(
            Radcheck.objects
            .using("radius")
            .filter(username=username)) > 0):
        return (False, "Username already exists.")

    Radcheck.objects.using("radius").create(
        username=username,
        attribute="SMD5-Password",
        op=":=",
        value=make_md5(password, settings.SALT_LENGTH))

    return (True, "Success!")


def change_password(username, password):
    """Change a user's password.

    Parameters
    ----------
    username : str
        Target user
    password : str
        New password

    Returns
    -------
    bool
        True if successful, False otherwise
    str
        Explanation of error
    """

    try:
        target = Radcheck.objects.using("radius").get(username=username)
        target.password = make_md5(password, settings.SALT_LENGTH)
        target.save()
        return (True, "Success!")

    except Radcheck.DoesNotExist:
        return (False, "User does not exist.")


def remove_user(username):
    """Remove a user account.

    Parameters
    ----------
    username : str
        User to remove.

    Returns
    -------
    bool
        True if successful, False otherwise
    str
        Explanation of error
    """

    try:
        Radcheck.objects.using("radius").get(username=username).delete()
        return (True, "Success!")

    except Radcheck.DoesNotExist:
        return (False, "User does not exist.")
