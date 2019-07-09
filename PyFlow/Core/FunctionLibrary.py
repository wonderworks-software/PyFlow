"""
.. sidebar:: **FunctionLibrary.py**

    This file contains decorator for implementing a node from python function.
    The main idea is to describe argument types and default values.

.. py:function:: IMPLEMENT_NODE(func=None, returns={}, meta={}, nodeType=NodeTypes.Pure) -> function


"""

try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec

from PyFlow.Core.Common import *

empty = {}


def IMPLEMENT_NODE(func=None, returns=empty, meta={'Category': 'Default', 'Keywords': []}, nodeType=NodeTypes.Pure):
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
            for (i, name) in enumerate(spec.args[-len(defaults):]):
                if len(defaults[i]) < 1 or defaults[i][0] is empty:
                    continue
                func.__annotations__[name] = defaults[i]
        return func

    if returns == empty:
        return wrapper(func)
    return wrapper


class FunctionLibraryBase(object):
    """Base class fo function libraries
    """

    def __init__(self, packageName):
        super(FunctionLibraryBase, self).__init__()
        self.__foos = {}
        for name, function in inspect.getmembers(self, inspect.isfunction):
            function.__annotations__["packageName"] = packageName
            function.__annotations__["lib"] = self.__class__.__name__
            self.__foos[name] = function

    def getFunctions(self):
        return self.__foos
