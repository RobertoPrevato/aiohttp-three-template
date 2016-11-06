import yaml
from collections import abc
from keyword import iskeyword


class Configuration:
    """
    Provides methods to handle configuration objects.
    A read-only façade for navigating configuration objects using attribute notation.

    Thanks to Fluent Python, book by Luciano Ramalho; this class is adapted from his example of JSON structure explorer.
    """

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __contains__(self, item):
        return item in self.__data

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return Configuration(self.__data[name])

    @classmethod
    def from_yaml(cls, filename):
        # NB: following line is blocking, however this operation is performed only at application start.
        # to read a file in non-blocking way, a library like aiofiles should be used.
        with open(filename, "rt") as f:
            data = yaml.load(f)
        return cls(data)
