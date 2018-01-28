from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Vector4(FunctionLibraryBase):
    '''doc string for Vector4'''
    def __init__(self):
        super(Vector4, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Create():
        '''Zero vector4.'''
        return pyrr.Vector4()

    @staticmethod
    @implementNode(returns=(DataTypes.String, str(pyrr.Vector4())), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4ToStr(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        return str(v)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenX():
        '''Unit length x vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_x())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenY():
        '''Unit length y vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_y())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenZ():
        '''Unit length z vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_z())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromUnitLenW():
        '''Unit length w vector4.'''
        return pyrr.Vector4(pyrr.vector4.create_unit_length_w())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromV3(v=(DataTypes.FloatVector3, pyrr.Vector4())):
        '''Creates vector4 from vector3.'''
        return pyrr.Vector4(pyrr.vector4.create_from_vector3(v))

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4X(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Returns x component of the vector4.'''
        return v.x

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Y(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Returns y component of the vector4.'''
        return v.y

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Z(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Returns z component of the vector4.'''
        return v.z

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4W(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Returns w component of the vector4.'''
        return v.w

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '+']})
    def v4Add(a=(DataTypes.FloatVector4, pyrr.Vector4()), b=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Adds vector4 a and b.'''
        return a + b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '-']})
    def v4Substract(a=(DataTypes.FloatVector4, pyrr.Vector4()), b=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Substracts vector a and b.'''
        return a - b

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '|']})
    def v4Dot(a=(DataTypes.FloatVector4, pyrr.Vector4()), b=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Dot product of two vectors.'''
        return a | b

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Lerp(a=(DataTypes.FloatVector4, pyrr.Vector4()), b=(DataTypes.FloatVector4, pyrr.Vector4([1.0, 1.0, 1.0, 1.0])), alpha=(DataTypes.Float, 0.0)):
        '''Vector4 lerp.'''
        return pyrr.Vector4(pyrr.vector.interpolate(a, b, clamp(alpha, 0.0, 1.0)))

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, True), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', '==']})
    def v4Equals(a=(DataTypes.FloatVector4, pyrr.Vector4()), b=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Check if vectors are equals.'''
        return a == b

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Len(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Returns the length of a vector.'''
        return pyrr.vector.length(v)

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector3', 'Keywords': ['vector4']})
    def v4SquaredLen(v=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Calculates the squared length of a vector.\nUseful when trying to avoid the performance penalty of a square root operation.'''
        return pyrr.vector.squared_length(v)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Normalize(v=(DataTypes.FloatVector4, pyrr.Vector4()), result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''Normalizes a single vector to unit length.\nIf zero-length - returns original one.'''
        try:
            res = pyrr.Vector4(pyrr.vector.normalize(v))
            result.setData(True)
            return res
        except:
            result.setData(False)
            return v

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4', 'resize']})
    def v4SetLen(v=(DataTypes.FloatVector4, pyrr.Vector4()), length=(DataTypes.Float, 0.0)):
        '''Resizes a vector to "length".'''
        return pyrr.Vector4(pyrr.vector.set_length(v, length))

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4Create(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0), W=(DataTypes.Float, 0.0)):
        '''Creates vector4 from given components.'''
        return pyrr.Vector4([a, b, c, W])

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Vector4', 'Keywords': ['vector4']})
    def v4FromM44Tr(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Create vector4 from matrix44 translation.'''
        return pyrr.Vector4(pyrr.vector4.create_from_matrix44_translation(m))
