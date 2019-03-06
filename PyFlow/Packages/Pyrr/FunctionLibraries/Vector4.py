import pyrr

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.Pyrr import PACKAGE_NAME


class Vector4(FunctionLibraryBase):
    packageName = PACKAGE_NAME
    '''doc string for Vector4'''
    def __init__(self):
        super(Vector4, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Create():
        '''Zero vector4.'''
        return pyrr.Vector4()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', str(pyrr.Vector4())), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4ToStr(v=('FloatVector4Pin', pyrr.Vector4())):
        return str(v)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenX():
        '''Unit length x vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_x())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenY():
        '''Unit length y vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_y())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenZ():
        '''Unit length z vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_z())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenW():
        '''Unit length w vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_w())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromV3(v=('FloatVector3Pin', pyrr.Vector4())):
        '''Creates vector4 from vector3.'''
        return pyrr.Vector4(pyrr.vector4.create_from_vector3(v))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4X(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Returns x component of the vector4.'''
        return v.x

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Y(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Returns y component of the vector4.'''
        return v.y

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Z(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Returns z component of the vector4.'''
        return v.z

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4W(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Returns w component of the vector4.'''
        return v.w

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '+']})
    def v4Add(a=('FloatVector4Pin', pyrr.Vector4()), b=('FloatVector4Pin', pyrr.Vector4())):
        '''Adds vector4 a and b.'''
        return a + b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '-']})
    def v4Substract(a=('FloatVector4Pin', pyrr.Vector4()), b=('FloatVector4Pin', pyrr.Vector4())):
        '''Substracts vector a and b.'''
        return a - b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '|']})
    def v4Dot(a=('FloatVector4Pin', pyrr.Vector4()), b=('FloatVector4Pin', pyrr.Vector4())):
        '''Dot product of two vectors.'''
        return a | b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Lerp(a=('FloatVector4Pin', pyrr.Vector4()), b=('FloatVector4Pin', pyrr.Vector4([1.0, 1.0, 1.0, 1.0])), alpha=('FloatPin', 0.0)):
        '''Vector4 lerp.'''
        return pyrr.Vector4(pyrr.vector.interpolate(a, b, clamp(alpha, 0.0, 1.0)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', True), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '==']})
    def v4Equals(a=('FloatVector4Pin', pyrr.Vector4()), b=('FloatVector4Pin', pyrr.Vector4())):
        '''Check if vectors are equals.'''
        return a == b

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Len(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Returns the length of a vector.'''
        return pyrr.vector.length(v)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector4']})
    def v4SquaredLen(v=('FloatVector4Pin', pyrr.Vector4())):
        '''Calculates the squared length of a vector.\nUseful when trying to avoid the performance penalty of a square root operation.'''
        return pyrr.vector.squared_length(v)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Normalize(v=('FloatVector4Pin', pyrr.Vector4()), result=("Reference", ('BoolPin', False))):
        '''Normalizes a single vector to unit length.\nIf zero-length - returns original one.'''
        try:
            res = pyrr.Vector4(pyrr.vector.normalize(v))
            result(True)
            return res
        except:
            result(False)
            return v

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', 'resize']})
    def v4SetLen(v=('FloatVector4Pin', pyrr.Vector4()), length=('FloatPin', 0.0)):
        '''Resizes a vector to "length".'''
        return pyrr.Vector4(pyrr.vector.set_length(v, length))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Create(a=('FloatPin', 0.0), b=('FloatPin', 0.0), c=('FloatPin', 0.0), W=('FloatPin', 0.0)):
        '''Creates vector4 from given components.'''
        return pyrr.Vector4([a, b, c, W])

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromM44Tr(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Create vector4 from matrix44 translation.'''
        return pyrr.Vector4(pyrr.vector4.create_from_matrix44_translation(m))
