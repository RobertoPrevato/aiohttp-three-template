def first(a, fn):
    """
    Example: first([3,4,5,6], lambda x: x > 4)

    :param a: array
    :param fn: function to evaluate items
    :return: None or first item matching result
    """
    return next((x for x in a if fn(x)), None)


def where(a, fn):
    """
    Example: where([3,4,5,6], lambda x: x > 4)

    Returns an array of items from an iterable, that respect the given condition.
    :param a: array
    :param fn: function to evaluate items
    :return: None or first item matching result
    """
    return [x for x in a if fn(x)]


def single(a, fn):
    """
    Returns a single item inside an iterable, respecting a given condition.
    Raises exception if more than one item, or no items respect the condition.
    Example: single([3,4,5,6], lambda x: x > 4)

    :param a: array
    :param fn: function to evaluate items
    :return: None or first item matching result
    """
    result = [x for x in a if fn(x)]
    if result is None or len(result) == 0:
        raise ValueError("sequence contains no element")
    if len(result) > 1:
        raise ValueError("sequence contains more than one element")
    return result[0]


def distinct(a, fn=None):
    """
    Given an iterable, returns an array of distinct results.
    Optionally, a matcher function can be specified.

    :param a:
    :param fn: function to evaluate items
    :return:
    """
    result = []
    b = [] if fn is not None else None
    for x in a:
        if fn is None:
            if x not in result:
                result.append(x)
        else:
            v = fn(x)
            if v not in b:
                b.append(v)
                result.append(x)
    return result
