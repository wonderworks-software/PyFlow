from inspect import getargspec
from AGraphCommon import *

empty = {}


def returns(annotation):
    def wrapper(func):
        func.__annotations__ = getattr(func, '__annotations__', {})
        if annotation is not empty:
            func.__annotations__['return'] = annotation
        return func
    return wrapper


def implementNode(func=None, returns=empty, meta={'Category': 'Default', 'Keywords': []}, nodeType=NodeTypes.Pure):
    def wrapper(func):
        func.__annotations__ = getattr(func, '__annotations__', {})
        func.__annotations__['nodeType'] = nodeType

        if not meta == empty:
            func.__annotations__['meta'] = meta

        if not returns == empty:
            func.__annotations__['return'] = returns

        defaults = func.__defaults__
        if defaults:
            spec = getargspec(func)

            nanno = len(defaults)
            for (i, name) in enumerate(spec.args[-nanno:]):
                if len(defaults[i]) < 1 or defaults[i][0] is empty:
                    continue
                if defaults[i][0] == DataTypes.Reference:
                    func.__annotations__[name] = defaults[i][1]
                else:
                    func.__annotations__[name] = defaults[i][0]

            # defaults = tuple((d[1] for d in func.__defaults__ if len(d) > 1))
            customDefaults = []
            for d in func.__defaults__:
                if len(d) > 1:
                    if isinstance(d[1], tuple):
                        customDefaults.append(d[1][1])
                    else:
                        customDefaults.append(d[1])
            # func.__defaults__ = defaults or None
            func.__defaults__ = tuple(customDefaults) or None
        return func

    if returns == empty:
        return wrapper(func)
    return wrapper


class FunctionLibraryBase(object):
    """doc string for FunctionLibraryBase"""
    def __init__(self):
        super(FunctionLibraryBase, self).__init__()
