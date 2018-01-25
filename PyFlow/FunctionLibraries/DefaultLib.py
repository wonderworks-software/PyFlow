from FunctionLibrary import *
from AGraphCommon import *
import os


class DefaultLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(DefaultLib, self).__init__()

    @staticmethod
    @annotated(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': ['print']})
    def pyprint(entity=(DataTypes.String, None)):
        '''print string'''
        print(entity)

    @staticmethod
    @annotated(returns=None, nodeType=NodeTypes.Callable, meta={'Category': 'DefaultLib', 'Keywords': []})
    def cls():
        '''cls cmd call'''
        os.system('cls')

    @staticmethod
    @annotated(returns=DataTypes.Bool, meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeBool(b=(DataTypes.Bool, False)):
        '''make simple boolean'''
        return b

    @staticmethod
    @annotated(returns=DataTypes.Int, meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeInt(i=(DataTypes.Int, 0)):
        '''make integer'''
        return i

    @staticmethod
    @annotated(returns=DataTypes.Float, meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeFloat(f=(DataTypes.Float, 0.0)):
        '''make floating point number'''
        return f

    @staticmethod
    @annotated(returns=DataTypes.String, meta={'Category': 'GenericTypes', 'Keywords': []})
    def makeString(s=(DataTypes.String, '')):
        '''make string'''
        return s

    # Conversions
    @staticmethod
    @annotated(returns=DataTypes.Int, meta={'Category': 'Conversion', 'Keywords': []})
    def boolToInt(b=(DataTypes.Bool, False)):
        return int(b)

    @staticmethod
    @annotated(returns=DataTypes.Bool, meta={'Category': 'Conversion', 'Keywords': []})
    def intToBool(i=(DataTypes.Int, 0)):
        return bool(i)

    @staticmethod
    @annotated(returns=DataTypes.Bool, meta={'Category': 'Conversion', 'Keywords': []})
    def floatToInt(f=(DataTypes.Float, 0.0)):
        return int(f)

    @staticmethod
    @annotated(returns=DataTypes.Bool, meta={'Category': 'Conversion', 'Keywords': []})
    def intToFloat(i=(DataTypes.Int, 0)):
        return float(i)

    @staticmethod
    @annotated(returns=DataTypes.String, meta={'Category': 'Conversion', 'Keywords': []})
    def intToString(i=(DataTypes.Int, 0)):
        return str(i)

    @staticmethod
    @annotated(returns=DataTypes.String, meta={'Category': 'Conversion', 'Keywords': []})
    def floatToString(f=(DataTypes.Float, 0.0)):
        return str(i)

    @staticmethod
    @annotated(returns=DataTypes.String, meta={'Category': 'Conversion', 'Keywords': []})
    def boolToString(b=(DataTypes.Bool, str(False))):
        return str(b)
