class InvalidOperation(Exception):
    """
    An exception risen in case of an operation that doesn't make sense in a certain context.
    """

class ConfigurationError(Exception):
    """
    An exception risen in case of an operation that doesn't make sense in a certain context.
    """

class ArgumentNullException(ValueError):
    """
    An exception risen when a null or empty parameter is not acceptable.
    """
    def __init__(self, param_name):
        super().__init__("Parameter cannot be null or empty: `%s`" % param_name)
