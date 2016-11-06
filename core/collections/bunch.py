
class Bunch:
    """
    The simple but handy "collector of a bunch of named stuff" class by Alex Martelli
    http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def get(self, name, default=None):
        return getattr(self, name, default)

    def merge(self, dictionary):
        for x in dictionary:
          setattr(self, x, dictionary[x])
