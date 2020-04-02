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


import os
import platform
from copy import copy, deepcopy
from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow import getHashableDataTypes
from PyFlow.Core.Common import *
from PyFlow.Core.PathsRegistry import PathsRegistry
from nine import IS_PYTHON2


PIN_ALLOWS_ANYTHING = {PinSpecifires.ENABLED_OPTIONS: PinOptions.AllowAny | PinOptions.ArraySupported | PinOptions.DictSupported}


class DefaultLib(FunctionLibraryBase):
    """Default library builting stuff, variable types and conversions
    """

    def __init__(self, packageName):
        super(DefaultLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported, PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1"}),
                    meta={NodeMeta.CATEGORY: 'Utils', NodeMeta.KEYWORDS: ['id'], NodeMeta.CACHE_ENABLED: False})
    def copyObject(obj=('AnyPin', None, {PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported, PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1"}), deepCopy=("BoolPin", False)):
        '''Shallow or deep copy of an object.'''
        copyFunction = deepcopy if deepCopy else copy
        return copyFunction(obj)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'Common', NodeMeta.KEYWORDS: []})
    def clearConsole():
        '''Cross platform clears console.'''
        system = platform.system()
        if system != "":
            system = system.lower()
            if system in ("windows", "win32"):
                os.system('cls')
            if system in ("linux", "darwin", "linux2"):
                os.system('clear')

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makeInt(i=('IntPin', 0)):
        '''Make integer.'''
        return i

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makeFloat(f=('FloatPin', 0.0)):
        '''Make floating point number.'''
        return f

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makeString(s=('StringPin', '')):
        '''Make string.'''
        return s

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={NodeMeta.CATEGORY: 'Common', NodeMeta.KEYWORDS: [],NodeMeta.CACHE_ENABLED: False})
    def setGlobalVar(name=('StringPin', 'var1'), value=('AnyPin', None, PIN_ALLOWS_ANYTHING.copy())):
        '''Sets value to globals() dict'''
        globals()[name] = value

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, PIN_ALLOWS_ANYTHING.copy()), meta={NodeMeta.CATEGORY: 'Common', NodeMeta.KEYWORDS: []})
    def getAttribute(obj=('AnyPin', None, PIN_ALLOWS_ANYTHING.copy()), name=('StringPin', 'attrName')):
        '''Returns attribute from object using "getattr(name)"'''
        return getattr(obj, name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, PIN_ALLOWS_ANYTHING.copy()), meta={NodeMeta.CATEGORY: 'Common', NodeMeta.KEYWORDS: [],NodeMeta.CACHE_ENABLED: False})
    def getGlobalVar(name=('StringPin', 'var1')):
        '''Retrieves value from globals()'''
        if name in globals():
            return globals()[name]
        else:
            return None

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makePath(path=('StringPin', '', {PinSpecifires.INPUT_WIDGET_VARIANT: "PathWidget"})):
        '''Make path.'''
        return path

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def makeBool(b=('BoolPin', False)):
        '''Make boolean.'''
        return b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0, {PinSpecifires.ENABLED_OPTIONS: PinOptions.AlwaysPushDirty}), meta={NodeMeta.CATEGORY: 'Utils', NodeMeta.KEYWORDS: [], NodeMeta.CACHE_ENABLED: False})
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of process_time().'''
        return currentProcessorTime()

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported}), meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: []})
    def select(A=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported}),
               B=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported}),
               PickA=('BoolPin', False),
               aPicked=(REF, ("BoolPin", False))):
        '''
        If bPickA is true, A is returned, otherwise B.
        '''
        aPicked(PickA)
        return A if PickA else B

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ""), meta={NodeMeta.CATEGORY: 'GenericTypes', NodeMeta.KEYWORDS: []})
    def objectType(obj=("AnyPin", None, {PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported})):
        '''Returns ``type(obj).__name__``'''
        t = type(obj).__name__
        if t == "DictElement":
            t += ",key:{0},value:{1}".format(type(obj[1]).__name__, type(obj[0]).__name__)
        return t

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: ['in'], NodeMeta.CACHE_ENABLED: False})
    def contains(obj=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported}), element=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1"})):
        """Python's **in** keyword. `element in obj` will be executed"""
        try:
            return element in obj
        except:
            return False

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0, {PinSpecifires.DESCRIPTION: "Number of elements of iterable"}), meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: ['len']})
    def len(obj=('AnyPin', None, {PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny | PinOptions.DictElementSupported, PinSpecifires.DESCRIPTION: "Iterable object"})):
        """Python's **len** function."""
        try:
            return len(obj)
        except:
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: ['get'], NodeMeta.CACHE_ENABLED: False})
    def getItem(obj=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                element=("AnyPin", None, {PinSpecifires.SUPPORTED_DATA_TYPES: getHashableDataTypes()}),
                result=(REF, ("BoolPin", False))):
        """Python's ``[]`` operator. ``obj[element]`` will be executed."""
        try:
            result(True)
            return obj[element]
        except:
            result(False)
            return None

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}), meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: ['get'], 'CacheEnabled': False})
    def appendTo(obj=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                 element=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1"}),
                 result=(REF, ('BoolPin', False))):
        """Calls ``obj.append(element)``. And returns object. If failed - object is unchanged"""
        try:
            obj.append(element)
            result(True)
            return obj
        except:
            result(False)
            return obj

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={NodeMeta.CATEGORY: 'DefaultLib', NodeMeta.KEYWORDS: ['get']})
    def addTo(obj=('AnyPin', None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
              element=("AnyPin", None, {PinSpecifires.CONSTRAINT: "1"}),
              result=(REF, ("AnyPin", None, {PinSpecifires.CONSTRAINT: "1", PinSpecifires.STRUCT_CONSTRAINT: "1", PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}))):
        """Calls ``obj.add(element)``. And returns object. If failed - object is unchanged"""
        try:
            obj.add(element)
            result(obj)
            return True
        except:
            result(obj)
            return False
