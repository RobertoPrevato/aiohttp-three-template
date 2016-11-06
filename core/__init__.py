from core.exceptions import ArgumentNullException


def has_params(data, *args):
    """
    Validates required parameters against an object.
    :param data:
    :param args: required parameters
    :return:
    """
    if data is None:
        return False
    for a in args:
        if not a in data:
            return False
        v = data[a]
        if v is None or v == "":
            return False
    return True


def require_params(*args, **kwargs):
    for name, value in kwargs.items():
        if value is None or value == "":
            raise ArgumentNullException(name)
    for a in args:
        if a is None or a == "":
            raise ArgumentNullException(a)
    return True