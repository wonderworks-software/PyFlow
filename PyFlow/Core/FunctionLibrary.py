"""
.. sidebar:: **FunctionLibrary.py**

    This file contains a decorator to turn pyton function into a node.
    And base class for funciton library.
    The main idea is to use function arguments as input and output pins.


.. py:function:: IMPLEMENT_NODE(func=None, returns={}, meta={}, nodeType=NodeTypes.Pure)

Detailed description
====================

We use this function as decorator in 100% cases.
See :file:`PyFlow/Packages/PyFlowBase/FunctionLibraries` content for plenty of examples

Arguments
---------

**func**

    Function to be annotated

**returns**

    Value  of this argument is tuple with 2 or 3 elements or None.
    First element is pin data type.
    Second - default value.
    Third element is :term:`pin specifires`

.. seealso:: :meth:`~PyFlow.Core.NodeBase.NodeBase.createInputPin`
             :meth:`~PyFlow.Core.NodeBase.NodeBase.createOutputPin`
             :class:`~PyFlow.Core.PinBase.PinBase`

**meta**

    Value of this argument is :term:`node meta`

**nodeType**

    Value of this argument is :class:`~PyFlow.Core.Common.NodeTypes`. If :attr:`~PyFlow.Core.Common.NodeTypes.Callable` specified
    input and output exec pins will be created.

Examples:
::

    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeInt(i=('IntPin', 0)):
        return i

    @IMPLEMENT_NODE(returns=('FloatPin', 0.0, {"enabledOptions": PinOptions.AlwaysPushDirty}))
    def clock():
        return time.clock()


.. glossary::

    pin specifires
        dict that describes different pin options and attributes to be considered on generation

        Following key-value pairs allowed:

        >>> ("supportedDataTypes" : list)
        >>> ("constraint": None)
        >>> ("structConstraint": None)
        >>> ("enabledOptions": None)
        >>> ("disabledOptions": None)
        >>> ("inputWidgetVariant": "DefaultWidget")

    node meta
        dict that describes different node options and attributes to be considered on generation

        Following key-value pairs allowed:

        >>> ("Category" : str)
        >>> ("Keywords" : [str])
        >>> ("CacheEnabled" : bool)

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
