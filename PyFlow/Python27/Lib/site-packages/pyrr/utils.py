# -*- coding: utf-8 -*-
"""Provides common utility functions.
"""
import inspect
from functools import wraps
import numpy as np


def all_parameters_as_numpy_arrays(fn):
    """Converts all of a function's arguments to numpy arrays.

    Used as a decorator to reduce duplicate code.
    """
    # wraps allows us to pass the docstring back
    # or the decorator will hide the function from our doc generator
    @wraps(fn)
    def wrapper(*args, **kwargs):
        args = list(args)
        for i, v in enumerate(args):
            if v is not None:
                args[i] = np.asarray(v)
        for k,v in kwargs.items():
            if v is not None:
                kwargs[k] = np.asarray(v)
        return fn(*args, **kwargs)
    return wrapper

def parameters_as_numpy_arrays(*args_to_convert):
    """Converts specific arguments to numpy arrays.

    Used as a decorator to reduce duplicate code.

    Arguments are specified by their argument name.
    For example
    ::

        @parameters_as_numpy_arrays('a', 'b', 'optional')
        def myfunc(a, b, *args, **kwargs):
            pass

        myfunc(1, [2,2], optional=[3,3,3])
    """
    def decorator(fn):
        # wraps allows us to pass the docstring back
        # or the decorator will hide the function from our doc generator

        try:
            getfullargspec = inspect.getfullargspec
        except AttributeError:
            getfullargspec = inspect.getargspec

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # get the arguements of the function we're decorating
            fn_args = getfullargspec(fn)

            # convert any values that are specified
            # if the argument isn't in our list, just pass it through

            # convert the *args list
            # we zip the args with the argument names we received from
            # the inspect function
            args = list(args)
            for i, (k, v) in enumerate(zip(fn_args.args, args)):
                if k in args_to_convert and v is not None:
                    args[i] = np.array(v)

            # convert the **kwargs dict
            for k,v in kwargs.items():
                if k in args_to_convert and v is not None:
                    kwargs[k] = np.array(v)

            # pass the converted values to our function
            return fn(*args, **kwargs)
        return wrapper
    return decorator
