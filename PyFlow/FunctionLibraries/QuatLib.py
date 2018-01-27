from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class QuatLib(FunctionLibraryBase):
    '''doc string for QuatLib'''
    def __init__(self):
        super(QuatLib, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def zeroQuat():
        '''Returns zero quaternion.'''
        return pyrr.Quaternion()

    @staticmethod
    @implementNode(returns=(DataTypes.String, ''), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatToString(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Convert to quat to str'''
        return str(q)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion.from_x_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromXRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the X-axis.'''
        return pyrr.Quaternion.from_x_rotation(theta)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion.from_y_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromYRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the Y-axis.'''
        return pyrr.Quaternion.from_y_rotation(theta)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion.from_z_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromZRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the Z-axis.'''
        return pyrr.Quaternion.from_z_rotation(theta)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion.from_matrix(pyrr.Matrix33())), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromMatrix33(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Creates a Quaternion from the specified Matrix33.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion.from_matrix(pyrr.Matrix44())), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromMatrix44(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Creates a Quaternion from the specified Matrix44.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromEulers(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_eulers([a, b, c])

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromInverseOfEulers(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_inverse_of_eulers([a, b, c])

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromAxisRotation(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0), theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the specified axis.'''
        return pyrr.Quaternion.from_axis_rotation([a, b, c], theta)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatApplyToVector(q=(DataTypes.Quaternion, pyrr.Quaternion()), v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Rotates a vector by a quaternion.'''
        return pyrr.Vector3(pyrr.quaternion.apply_to_vector(quat=q, vec=v))

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatX(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the x component of the quat.'''
        return q.x

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatY(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the y component of the quat.'''
        return q.y

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatZ(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the z component of the quat.'''
        return q.z

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatW(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the w component of the quat.'''
        return q.w

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAngle(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the angle around the axis of rotation of this Quaternion as a float.'''
        return q.angle

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAxis(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the axis of rotation of this Quaternion as a Vector3.'''
        return q.axis

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatConjugate(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the conjugate of this Quaternion.\nThis is a Quaternion with the opposite rotation.'''
        return q.conjugate

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatCross(q=(DataTypes.Quaternion, pyrr.Quaternion()), other=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the cross of this Quaternion and another.\nThis is the equivalent of combining Quaternion rotations (like Matrix multiplication).'''
        return q.cross(other)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatDot(q=(DataTypes.Quaternion, pyrr.Quaternion()), other=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the dot of this Quaternion and another.'''
        return q.dot(other)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatInverse(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the inverse of this quaternion.'''
        return q.inverse

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatIsIdentity(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns True if the Quaternion has no rotation (0.,0.,0.,1.).'''
        return q.is_identity

    @staticmethod
    @implementNode(returns=(DataTypes.Float, False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatLength(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the length of this Quaternion.'''
        return q.length

    @staticmethod
    @implementNode(returns=(DataTypes.Float, False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatSquaredLength(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Calculates the squared length of a quaternion.\nUseful for avoiding the performanc penalty of the square root function.'''
        return pyrr.quaternion.squared_length(q)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatLerp(q1=(DataTypes.Quaternion, pyrr.Quaternion()), q2=(DataTypes.Quaternion, pyrr.Quaternion()), t=(DataTypes.Float, 0.0)):
        '''Interpolates between q1 and q2 by t. The parameter t is clamped to the range [0, 1].'''
        return q1.lerp(q2, t)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAsMatrix33(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns a Matrix33 representation of this Quaternion.'''
        return q.matrix33

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAsMatrix44(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns a Matrix44 representation of this Quaternion.'''
        return q.matrix44

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatNegative(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns the negative of the Quaternion.'''
        return q.negative

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatNormalize(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Returns a normalized version of this Quaternion as a new Quaternion.'''
        return q.normalized

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatPower(q=(DataTypes.Quaternion, pyrr.Quaternion()), exp=(DataTypes.Float, 0.0), result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''Returns a new Quaternion representing this Quaternion to the power of the exponent. Checks for identify quaternion'''
        try:
            powered = q.power(exp)
            result.setData(True)
        except:
            result.setData(False)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatSlerp(q1=(DataTypes.Quaternion, pyrr.Quaternion()), q2=(DataTypes.Quaternion, pyrr.Quaternion()), t=(DataTypes.Float, 0.0)):
        '''Spherically interpolates between quat1 and quat2 by t. The parameter t is clamped to the range [0, 1].'''
        return q1.slerp(q2, t)

    @staticmethod
    @implementNode(returns=(DataTypes.Bool, False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatIsZeroLength(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Checks if a quaternion is zero length.'''
        return pyrr.quaternion.is_zero_length(q)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': ['*']})
    def quatMult(q1=(DataTypes.Quaternion, pyrr.Quaternion()), q2=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''"*" operator for quaternions.'''
        return q1 * q2
