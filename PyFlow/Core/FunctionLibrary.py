## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


"""
.. sidebar:: **FunctionLibrary.py**

    This file contains a decorator to turn python function into a node.
    And base class for function library.
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

    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makeInt(i=('IntPin', 0)):
        return i

    @IMPLEMENT_NODE(returns=('FloatPin', 0.0, {PinSpecifires.ENABLED_OPTIONS: PinOptions.AlwaysPushDirty}))
    def clock():
        return time.processor_time()


.. glossary::

    pin specifires
        dict that describes different pin options and attributes to be considered on generation

        Following key-value pairs allowed:

        >>> (PinSpecifires.SUPPORTED_DATA_TYPES : list)
        >>> (PinSpecifires.CONSTRAINT: None)
        >>> (PinSpecifires.STRUCT_CONSTRAINT: None)
        >>> (PinSpecifires.ENABLED_OPTIONS: None)
        >>> (PinSpecifires.DISABLED_OPTIONS: None)
        >>> (PinSpecifires.INPUT_WIDGET_VARIANT: "DefaultWidget")
        >>> (PinSpecifires.DESCRIPTION: str)
        >>> (PinSpecifires.VALUE_LIST: [str])
        >>> (PinSpecifires.VALUE_RANGE: (int|float, int|float))
        >>> (PinSpecifires.DRAGGER_STEPS: [int|float])

        Value list is specific for string pins. If Specified - enum input widget will be created for this pin.
        If value range is specified, slider will be created in property view instead of value box.
        Dragger steps is a list of values which will be used in value dragger (middle mouse button).


    node meta
        dict that describes different node options and attributes to be considered on generation

        Following key-value pairs allowed:

        >>> ("Category" : str)
        >>> ("Keywords" : [str])
        >>> ("CacheEnabled" : bool)

"""

from inspect import getfullargspec, getmembers, isfunction

from PyFlow.Core.Common import *

empty = {}


def IMPLEMENT_NODE(
    func=None,
    returns=empty,
    meta={NodeMeta.CATEGORY: "Default", NodeMeta.KEYWORDS: []},
    nodeType=NodeTypes.Pure,
):
    def wrapper(func):
        func.__annotations__ = getattr(func, "__annotations__", {})
        func.__annotations__["nodeType"] = nodeType

        if not meta == empty:
            func.__annotations__["meta"] = meta

        if not returns == empty:
            func.__annotations__["return"] = returns

        defaults = func.__defaults__
        if defaults:
            spec = getfullargspec(func)
            for i, name in enumerate(spec.args[-len(defaults):]):
                if len(defaults[i]) < 1 or defaults[i][0] is empty:
                    continue
                func.__annotations__[name] = defaults[i]
        return func

    if returns == empty:
        return wrapper(func)
    return wrapper


class FunctionLibraryBase(object):
    """Base class fo function libraries"""

    def __init__(self, packageName):
        super(FunctionLibraryBase, self).__init__()
        self.__foos = {}
        for name, function in getmembers(self, isfunction):
            function.__annotations__["packageName"] = packageName
            function.__annotations__["lib"] = self.__class__.__name__
            self.__foos[name] = function

    def getFunctions(self):
        return self.__foos
