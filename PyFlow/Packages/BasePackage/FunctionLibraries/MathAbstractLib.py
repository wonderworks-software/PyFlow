from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.BasePackage import PACKAGE_NAME

class MathAbstractLib(FunctionLibraryBase):
    '''doc string for MathAbstractLib'''
    def __init__(self):
        super(MathAbstractLib, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["="]}, packageName=PACKAGE_NAME)
    ## Is a equal b
    def isequal(a=("AnyPin", 0,{"constraint":"1"}),
                b=("AnyPin", 0,{"constraint":"1"})):
        '''
        Is a equal b
        '''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">"]}, packageName=PACKAGE_NAME)
    ## Is a > b
    def isGreater(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                  b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Is a > b
        '''
        return a > b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': [">"]}, packageName=PACKAGE_NAME)
    ## Is a >= b
    def isGreaterOrEqual(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                         b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Is a >= b
        '''
        return a >= b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]}, packageName=PACKAGE_NAME)
    ## Is a < b
    def isLess(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
               b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Is a < b
        '''
        return a < b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Basic', 'Keywords': ["<"]}, packageName=PACKAGE_NAME)
    ## Is a <= b
    def isLessOrEqual(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                         b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Is a <= b
        '''
        return a <= b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['+', 'append',"sum"]}, packageName=PACKAGE_NAME)
    ## Basic Sum 
    def add(a=("AnyPin", 0,{"constraint":"1"}), b=("AnyPin", 0,{"constraint":"1"})):
        '''
        Basic Sum 
        '''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['-']}, packageName=PACKAGE_NAME)
    ## Basic subtraction
    def subtract(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                         b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Basic subtraction
        '''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=("AnyPin", 0.0,{"constraint":"1"}), meta={'Category': 'Math|Basic', 'Keywords': ['/',"divide"]}, packageName=PACKAGE_NAME)
    ## Basic division
    def divide(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                         b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                         result=("Reference", ("BoolPin", False))):
        '''
        Basic division
        '''
        try:
            d = a / b
            result(True)
            return d
        except:
            result(False)
            return -1

    @staticmethod
    @IMPLEMENT_NODE(returns=(("AnyPin", 0,{"constraint":"1"})), meta={'Category': 'Math|Basic', 'Keywords': ['*',"multiply"]}, packageName=PACKAGE_NAME)
    ## Basic multiplication
    def multiply(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
             b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]})):
        '''
        Basic multiplication
        '''
        return a * b
       

    @staticmethod
    @IMPLEMENT_NODE(returns=("FloatPin", 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector', '|','dot','product']}, packageName=PACKAGE_NAME)
    def dotProduct(a=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["FloatVector4Pin","FloatVector3Pin","QuatlPin"]}),
              b=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["FloatVector4Pin","FloatVector3Pin","QuatlPin"]})):
        '''Dot product'''
        if type(a) == "Quaternion":
            return a.dot(b)
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=("BoolPin", False), meta={'Category': 'Math|Int', 'Keywords': ["inrange","range"]}, packageName=PACKAGE_NAME)
    def inRange(Value=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                RangeMin=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                RangeMax=("AnyPin", 0,{"constraint":"1","supportedDataTypes":["BoolPin","FloatPin","IntPin",
                                                                              "Matrix33Pin","Matrix44Pin","QuatlPin",
                                                                              "FloatVector3Pin","FloatVector4Pin"]}),
                InclusiveMin=("BoolPin", False),
                InclusiveMax=("BoolPin", False)):
        '''
        Returns true if value is between Min and Max (V &gt;= Min && V &lt;= Max) If InclusiveMin is true, value needs to be equal or larger than Min, else it needs to be larger If InclusiveMax is true, value needs to be smaller or equal than Max, else it needs to be smaller
        '''
        return ((Value >= RangeMin) if InclusiveMin else (Value > RangeMin)) and ((Value <= RangeMax) if InclusiveMax else (Value < RangeMax))        