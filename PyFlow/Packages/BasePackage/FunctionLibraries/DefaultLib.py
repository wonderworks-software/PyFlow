import os
import platform

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class DefaultLib(FunctionLibraryBase):
    packageName = PACKAGE_NAME
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(DefaultLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': ['print']})
    ## Python's 'print' function wrapper
    def pyprint(entity=('AnyPin', None)):
        '''
        printing a string
        '''
        print(str(entity))

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []})
    ## cls cmd call.
    def clearConsole():
        '''clears console.'''
        if platform.system() == "Windows":
            os.system('cls')
        if platform.system() == "Linux":
            os.system('clear')

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'GenericTypes', 'Keywords': []})
    ## make integer
    def makeInt(i=('IntPin', 0)):
        '''make integer'''
        return i
    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'GenericTypes', 'Keywords': []})
    ## make floating point number
    def makeFloat(f=('FloatPin', 0.0)):
        '''make floating point number'''
        return f
    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'GenericTypes', 'Keywords': []})
    ## make string
    def makeString(s=('StringPin', '')):
        '''make string'''
        return s
    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Bool', 'Keywords': []})
    ## make simple boolean
    def makeBool(b=('BoolPin', False)):
        '''
        make boolean
        '''
        return b

    # Conversions
    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Conversion', 'Keywords': ["Bool"]})
    def toBool(i=('AnyPin', 0,{"supportedDataTypes":["BoolPin","FloatPin","IntPin"]})):
        return bool(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=("IntPin", 0), meta={'Category': 'Conversion', 'Keywords': []})
    def toInt(i=('AnyPin', 0,{"supportedDataTypes":["BoolPin","FloatPin","IntPin"]})):
        return int(f)

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", False), meta={'Category': 'Conversion', 'Keywords': []})
    def toFloat(i=('AnyPin', 0,{"supportedDataTypes":["BoolPin","FloatPin","IntPin"]})):
        return float(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=("StringPin", ''), meta={'Category': 'Conversion', 'Keywords': []})
    def toString(i=('AnyPin', 0)):
        return str(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', 0,{"constraint":"1"}), meta={'Category': 'Conversion', 'Keywords': []})
    def passtrhough(input=('AnyPin', 0,{"constraint":"1"})):
        return input  


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Utils', 'Keywords': []})
    ## Returns the CPU time or real time since the start of the process or since the first call of clock()
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of clock().'''
        return time.clock()
