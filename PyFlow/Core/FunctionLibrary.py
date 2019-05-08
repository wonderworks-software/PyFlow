"""@file FunctionLibrary.py

This file contains decorator for implementing node from function.

The main idea is to describe argument types and default values.

Using this information it becomes possible to create pins according to arguments types.
"""
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec

from PyFlow.Core.Common import *

empty = {}


# Turns function into a node
# @param[in] func decorated function
# @param[in] returns it can be tuple with [data type identifier](@ref PyFlow.Core.Common.DataTypes) + default value, or None
# @param[in] meta dictionary with category path, keywords and any additional info
# @param[in] nodeType determines wheter it is a Pure node or Callable. If Callable - input and output execution pins will be created
# @sa [NodeTypes](@ref PyFlow.Core.Common.NodeTypes) FunctionLibraries
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


# Base class for all function libraries
# some common utilities can be moved here in future
class FunctionLibraryBase(object):
    def __init__(self, packageName):
        super(FunctionLibraryBase, self).__init__()
        self.__foos = {}
        for name, function in inspect.getmembers(self, inspect.isfunction):
            function.__annotations__["packageName"] = packageName
            function.__annotations__["lib"] = self.__class__.__name__
            self.__foos[name] = function

    def getFunctions(self):
        return self.__foos
