import pyrr

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *


class Matrix33(FunctionLibraryBase):
    '''doc string for Matrix33'''
    def __init__(self,packageName):
        super(Matrix33, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    ## Zero matrix33
    def m33Zero():
        '''Zero matrix33.'''
        return pyrr.Matrix33()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', str(pyrr.Matrix33())), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Matrix33 to string
    def m33ToStr(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Matrix33 to string.'''
        return str(m)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33.identity()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Identity matrix33
    def m33Ident():
        '''Identity matrix33.'''
        return pyrr.Matrix33.identity()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns first column of matrix
    def m33c1(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns first column of matrix.'''
        return pyrr.Vector3(m.c1)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns second column of matrix
    def m33c2(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns second column of matrix.'''
        return pyrr.Vector3(m.c2)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns third column of matrix
    def m33c3(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns third column of matrix.'''
        return pyrr.Vector3(m.c3)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns first row of matrix
    def m33r1(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns first row of matrix.'''
        return pyrr.Vector3(m.r1)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns second row of matrix
    def m33r2(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns second row of matrix.'''
        return pyrr.Vector3(m.r2)

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns third row of matrix
    def m33r3(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns third row of matrix.'''
        return pyrr.Vector3(m.r3)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns a Quaternion representing this matrix
    def m33quat(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns a Quaternion representing this matrix.'''
        return m.quaternion

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns a Matrix44 representing this matrix
    def m33ToM44(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns a Matrix44 representing this matrix.'''
        return m.matrix44

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns single scalar from matrix33. r and c taken as abs and clamped in range 1-3
    #  \param r: matrix row
    #  \param c: matrix column
    def m33GetComp(m=('Matrix33Pin', pyrr.Matrix33()), r=('IntPin', 1), c=('IntPin', 1)):
        '''Returns single scalar from matrix33. r and c taken as abs and clamped in range 1-3.'''
        _r = clamp(abs(r), 1, 3)
        _c = clamp(abs(c), 1, 3)
        name = 'm{0}{1}'.format(_r, _c)
        return getattr(m, name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33', 'quat']})
    ## Creates matrix33 from given quaternion
    def m33FromQuat(q=('QuatPin', pyrr.Quaternion())):
        '''Creates matrix33 from given quaternion.'''
        return pyrr.Matrix33(q)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33', '*']})
    ## Multiplies two m33 matrices m1 by m2
    def m33MultM33(m1=('Matrix33Pin', pyrr.Matrix33()), m2=('Matrix33Pin', pyrr.Matrix33())):
        '''Multiplies two m33 matrices m1 by m2.'''
        return m1 * m2

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33', '*']})
    def m33MultM44(m1=('Matrix33Pin', pyrr.Matrix33()), m2=('Matrix44Pin', pyrr.Matrix44())):
        '''Multiplies m33 by m44.\nm1 - m33\nm2 - m44.'''
        return m1 * m2

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33ApplyToV3(m=('Matrix33Pin', pyrr.Matrix33()), v=('FloatVector3Pin', pyrr.Vector3())):
        '''The matrix rotation are applied to the vector.\nReturns the vectors rotated by the specified matrix.'''
        return pyrr.Vector3(pyrr.matrix33.apply_to_vector(m, v))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33DirectionScale(v=('FloatVector3Pin', pyrr.Vector3()), s=('FloatPin', 0.0)):
        '''Creates a matrix which can apply a directional scaling to a set of vectors.\nAn example usage for this is to flatten a mesh against a single plane.\nReturns the scaling matrix.'''
        return pyrr.Matrix33(pyrr.matrix33.create_direction_scale(v, s))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromAxisAngle(axis=('FloatVector3Pin', pyrr.Vector3()), theta=('FloatPin', 0.0)):
        '''Creates a matrix from the specified theta rotation around an axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_axis_rotation(axis, theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromEulers(eulers=('FloatVector3Pin', pyrr.Vector3())):
        '''Creates a matrix from the specified Euler rotations.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_eulers(eulers))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromInvOfQuat(q=('QuatPin', pyrr.Quaternion())):
        '''Creates a matrix with the inverse rotation of a quaternion.\nReturns a matrix with shape (3,3) that respresents the inverse of the quaternion.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_inverse_of_quaternion(q))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33From44(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Creates a Matrix33 from a Matrix44.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_matrix44(m))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromScale(s=('FloatVector3Pin', pyrr.Vector3([1, 1, 1]))):
        '''Creates an identity matrix with the scale set.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_scale(s))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromX(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the X axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_x_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromY(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the Y axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_y_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromZ(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the Z axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_z_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix33Pin', pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33Inverse(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Returns the inverse of the matrix.\nThis is essentially a wrapper around numpy.linalg.inv.'''
        return m.inverse
