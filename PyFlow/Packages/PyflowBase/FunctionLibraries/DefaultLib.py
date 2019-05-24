import os
import platform
from copy import copy, deepcopy
from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class DefaultLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self, packageName):
        super(DefaultLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported,"constraint":"1","structConstraint":"1"}), meta={'Category': 'GenericTypes', 'Keywords': ['id']})
    def copyObject(obj=('AnyPin', None, {"enabledOptions": PinOptions.ArraySupported,"constraint":"1","structConstraint":"1"}), deepCopy=("BoolPin", False)):
        '''Shallow or deep copy of an object.'''
        copyFunction = deepcopy if deepCopy else copy
        return copyFunction(obj)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []})
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
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeInt(i=('IntPin', 0)):
        '''Make integer.'''
        return i

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeFloat(f=('FloatPin', 0.0)):
        '''Make floating point number.'''
        return f

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeString(s=('StringPin', '')):
        '''Make string.'''
        return s

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    def makeBool(b=('BoolPin', False)):
        '''Make boolean.'''
        return b

    # Conversions
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Conversion', 'Keywords': ["Bool"]})
    def toBool(i=('AnyPin', 0, {"supportedDataTypes": ["BoolPin", "FloatPin", "IntPin"]})):
        return bool(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=("IntPin", 0), meta={'Category': 'Conversion', 'Keywords': []})
    def toInt(i=('AnyPin', 0, {"supportedDataTypes": ["BoolPin", "FloatPin", "IntPin"]})):
        return int(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", False), meta={'Category': 'Conversion', 'Keywords': []})
    def toFloat(i=('AnyPin', 0, {"supportedDataTypes": ["BoolPin", "FloatPin", "IntPin"]})):
        return float(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ''), meta={'Category': 'Conversion', 'Keywords': []})
    def toString(i=('AnyPin', 0)):
        return str(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0, {"enabledOptions": PinOptions.AlwaysPushDirty}), meta={'Category': 'Utils', 'Keywords': []})
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of clock().'''
        return time.clock()
