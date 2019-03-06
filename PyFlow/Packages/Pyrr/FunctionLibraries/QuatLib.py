import pyrr

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *

class QuatLib(FunctionLibraryBase):
    '''doc string for QuatLib'''
    def __init__(self,packageName):
        super(QuatLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def zeroQuat():
        '''Returns zero quaternion.'''
        return pyrr.Quaternion()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', ''), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatToString(q=('QuatPin', pyrr.Quaternion())):
        '''Convert to quat to str'''
        return str(q)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion.from_x_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromXRotation(theta=('FloatPin', 0.0)):
        '''Creates a new Quaternion with a rotation around the X-axis.'''
        return pyrr.Quaternion.from_x_rotation(theta)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion.from_y_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromYRotation(theta=('FloatPin', 0.0)):
        '''Creates a new Quaternion with a rotation around the Y-axis.'''
        return pyrr.Quaternion.from_y_rotation(theta)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion.from_z_rotation(0.0)), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromZRotation(theta=('FloatPin', 0.0)):
        '''Creates a new Quaternion with a rotation around the Z-axis.'''
        return pyrr.Quaternion.from_z_rotation(theta)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion.from_matrix(pyrr.Matrix33())), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromMatrix33(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Creates a Quaternion from the specified Matrix33.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion.from_matrix(pyrr.Matrix44())), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromMatrix44(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Creates a Quaternion from the specified Matrix44.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromEulers(a=('FloatPin', 0.0), b=('FloatPin', 0.0), c=('FloatPin', 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_eulers([a, b, c])

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromInverseOfEulers(a=('FloatPin', 0.0), b=('FloatPin', 0.0), c=('FloatPin', 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_inverse_of_eulers([a, b, c])

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatFromAxisRotation(a=('FloatPin', 0.0), b=('FloatPin', 0.0), c=('FloatPin', 0.0), theta=('FloatPin', 0.0)):
        '''Creates a new Quaternion with a rotation around the specified axis.'''
        return pyrr.Quaternion.from_axis_rotation([a, b, c], theta)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatApplyToVector(q=('QuatPin', pyrr.Quaternion()), v=('FloatVector3Pin', pyrr.Vector3())):
        '''Rotates a vector by a quaternion.'''
        return pyrr.Vector3(pyrr.quaternion.apply_to_vector(quat=q, vec=v))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatX(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the x component of the quat.'''
        return q.x

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatY(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the y component of the quat.'''
        return q.y

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatZ(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the z component of the quat.'''
        return q.z

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatW(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the w component of the quat.'''
        return q.w

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAngle(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the angle around the axis of rotation of this Quaternion as a float.'''
        return q.angle

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAxis(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the axis of rotation of this Quaternion as a Vector3.'''
        return q.axis

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatConjugate(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the conjugate of this Quaternion.\nThis is a Quaternion with the opposite rotation.'''
        return q.conjugate

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatCross(q=('QuatPin', pyrr.Quaternion()), other=('QuatPin', pyrr.Quaternion())):
        '''Returns the cross of this Quaternion and another.\nThis is the equivalent of combining Quaternion rotations (like Matrix multiplication).'''
        return q.cross(other)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatDot(q=('QuatPin', pyrr.Quaternion()), other=('QuatPin', pyrr.Quaternion())):
        '''Returns the dot of this Quaternion and another.'''
        return q.dot(other)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatInverse(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the inverse of this quaternion.'''
        return q.inverse

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatIsIdentity(q=('QuatPin', pyrr.Quaternion())):
        '''Returns True if the Quaternion has no rotation (0.,0.,0.,1.).'''
        return q.is_identity

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatLength(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the length of this Quaternion.'''
        return q.length

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatSquaredLength(q=('QuatPin', pyrr.Quaternion())):
        '''Calculates the squared length of a quaternion.\nUseful for avoiding the performanc penalty of the square root function.'''
        return pyrr.quaternion.squared_length(q)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatLerp(q1=('QuatPin', pyrr.Quaternion()), q2=('QuatPin', pyrr.Quaternion()), t=('FloatPin', 0.0)):
        '''Interpolates between q1 and q2 by t. The parameter t is clamped to the range [0, 1].'''
        return q1.lerp(q2, t)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAsMatrix33(q=('QuatPin', pyrr.Quaternion())):
        '''Returns a Matrix33 representation of this Quaternion.'''
        return q.matrix33

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatAsMatrix44(q=('QuatPin', pyrr.Quaternion())):
        '''Returns a Matrix44 representation of this Quaternion.'''
        return q.matrix44

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatNegative(q=('QuatPin', pyrr.Quaternion())):
        '''Returns the negative of the Quaternion.'''
        return q.negative

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatNormalize(q=('QuatPin', pyrr.Quaternion())):
        '''Returns a normalized version of this Quaternion as a new Quaternion.'''
        return q.normalized

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatPower(q=('QuatPin', pyrr.Quaternion()), exp=('FloatPin', 0.0), result=("Reference", ('BoolPin', False))):
        '''Returns a new Quaternion representing this Quaternion to the power of the exponent. Checks for identify quaternion'''
        try:
            powered = q.power(exp)
            result(True)
            return powered
        except:
            result(False)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatSlerp(q1=('QuatPin', pyrr.Quaternion()), q2=('QuatPin', pyrr.Quaternion()), t=('FloatPin', 0.0)):
        '''Spherically interpolates between quat1 and quat2 by t. The parameter t is clamped to the range [0, 1].'''
        return q1.slerp(q2, t)

    @staticmethod
    @IMPLEMENT_NODE(returns=('BoolPin', False), meta={'Category': 'Math|Quaternion', 'Keywords': []})
    def quatIsZeroLength(q=('QuatPin', pyrr.Quaternion())):
        '''Checks if a quaternion is zero length.'''
        return pyrr.quaternion.is_zero_length(q)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Quaternion', 'Keywords': ['*']})
    def quatMult(q1=('QuatPin', pyrr.Quaternion()), q2=('QuatPin', pyrr.Quaternion())):
        '''"*" operator for quaternions.'''
        return q1 * q2
