import os
import platform

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME


class DefaultLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(DefaultLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': ['print']}, packageName=PACKAGE_NAME)
    ## Python's 'print' function wrapper
    def pyprint(entity=('StringPin', None)):
        '''
        printing a string
        '''
        print(entity)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## cls cmd call.
    def clearConsole():
        '''clears console.'''
        if platform.system() == "Windows":
            os.system('cls')
        if platform.system() == "Linux":
            os.system('clear')

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'GenericTypes', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## make integer
    def makeInt(i=('IntPin', 0)):
        '''make integer'''
        return i

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'GenericTypes', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## make floating point number
    def makeFloat(f=('FloatPin', 0.0)):
        '''make floating point number'''
        return f

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'GenericTypes', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## make string
    def makeString(s=('StringPin', '')):
        '''make string'''
        return s

    # Conversions
    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Conversion', 'Keywords': []}, packageName=PACKAGE_NAME)
    def intToBool(i=('IntPin', 0)):
        return bool(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', 0), meta={'Category': 'Conversion', 'Keywords': []}, packageName=PACKAGE_NAME)
    def floatToInt(f=('FloatPin', 0.0)):
        return int(f)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Utils', 'Keywords': []}, packageName=PACKAGE_NAME)
    ## Returns the CPU time or real time since the start of the process or since the first call of clock()
    def clock():
        '''Returns the CPU time or real time since the start of the process or since the first call of clock().'''
        return time.clock()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', False), meta={'Category': 'Conversion', 'Keywords': []}, packageName=PACKAGE_NAME)
    def intToFloat(i=('IntPin', 0)):
        return float(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Conversion', 'Keywords': []}, packageName=PACKAGE_NAME)
    def intToString(i=('IntPin', 0)):
        return str(i)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Conversion', 'Keywords': []}, packageName=PACKAGE_NAME)
    def floatToString(f=('FloatPin', 0.0)):
        return str(f)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin','',{"constraint":"1"}), meta={'Category': 'Conversion', 'Keywords': []},packageName=PACKAGE_NAME)
    def passtrhough(input=('AnyPin','',{"constraint":"1"})):
        return input