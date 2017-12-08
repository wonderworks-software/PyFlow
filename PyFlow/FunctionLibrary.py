from inspect import getargspec
from AGraphCommon import *

empty = {}


def returns(annotation):
    """
    Decorator to add ``annotation`` to ``func``'s ``return``
    annotation, as though it were a Python 3 ``-> ...`` annotation.
        >>> from anodi import returns
        >>> @returns(int)
        ... def example ():
        ...    pass
        ...
        >>> example.__annotations__
        {'return': <type 'int'>}
    """
    def annotate(func):
        func.__annotations__ = getattr(func, '__annotations__', {})
        if annotation is not empty:
            func.__annotations__['return'] = annotation
        return func
    return annotate


def annotated(func=None, returns=empty, meta={'Category': 'Default', 'Keywords': []}, nodeType=NodeTypes.Pure):
    """
    Decorator to treat ``func``'s default args as a combination of
    annotations and default values, migrating the annotations to
    ``func.__annotations__``, leaving only the defaults in
    ``__defaults__``).
    The optional ``returns`` keyword parameter is placed in the
    resulting ``__annotations__`` dict.
    Each default value must be a tuple, ``(annotation, default)``. To
    supply an unannotated parameter with a default value, use the
    ``empty`` marker object. To supply an annotation without a
    default value, use a 1-tuple: ``(annotation,)``.
    Note that the Python 2.x rules prohibiting non-default parameters
    from coming after defaults still apply, but we don't enforce those
    rules. The effect of using the ``(annotation,)`` form *after*
    using the ``(annotation, default)`` form is likely to be
    surprising, at best.
    You may specify an unannotated parameter by using an empty tuple
    as its default value. This is to allow placing unannotated
    parameters after annotated parameters. Ordinarily, this would not
    be allowed, since the annotated parameter would mark the start of
    default values, requiring defaults on all subsequent parameters.
    We do *not* support nested tuple parameters.
    We also don't yet have a way to add annotations to the ``*args``
    or ``**kwargs`` catch-all parameters, since they don't take
    defaults.
    Example:
        >>> from anodi import annotated, empty
        >>> @annotated
        ... def example (a, b, c=(int,), d=(), e=(empty, "hi")):
        ...    pass
        ...
        >>> example.__annotations__
        {'c': <type 'int'>}
        >>> example.__defaults__
        ('hi',)
        >>> @annotated(returns=int)
        ... def example (a, b, c=(int,), d=(), e=(empty, "hi")):
        ...    pass
        ...
        >>> example.__annotations__
        {'c': <type 'int'>, 'return': <type 'int'>}
        >>> example.__defaults__
        ('hi',)
    """

    def annotate(func):
        func.__annotations__ = getattr(func, '__annotations__', {})
        func.__annotations__['nodeType'] = nodeType

        if not meta == empty:
            func.__annotations__['meta'] = meta

        if not returns == empty:
            func.__annotations__['return'] = returns

        defaults = func.__defaults__
        if defaults:
            spec = getargspec(func)
            # ___TODO:___ support *args, **kwargs annotation?

            # extract annotations
            nanno = len(defaults)
            for (i, name) in enumerate(spec.args[-nanno:]):
                if len(defaults[i]) < 1 or defaults[i][0] is empty:
                    continue
                func.__annotations__[name] = defaults[i][0]

            # prune annotations, leaving only defaults
            defaults = tuple((d[1]
                              for d in func.__defaults__
                              if len(d) > 1))
            # use ``None`` if there are no defaults left, since that's
            # how a function without any defaults would come out.
            func.__defaults__ = defaults or None
        return func

    # if we were called without a ``results`` argument, then we're
    # directly decorating ``func``:
    if returns == empty:
        return annotate(func)

    # otherwise, we're indirectly decorating, via ``annotate``:
    return annotate


class FunctionLibraryBase(object):
    """doc string for FunctionLibraryBase"""
    def __init__(self):
        super(FunctionLibraryBase, self).__init__()
