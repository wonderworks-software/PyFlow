from Core.FunctionLibrary import *
from Core.AGraphCommon import *
import pyrr


class Matrix33(FunctionLibraryBase):
    '''doc string for Matrix33'''
    def __init__(self):
        super(Matrix33, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    ## Zero matrix33
    def m33Zero():
        '''Zero matrix33.'''
        return pyrr.Matrix33()

    @staticmethod
    @implementNode(returns=(DataTypes.String, str(pyrr.Matrix33())), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Matrix33 to string
    def m33ToStr(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Matrix33 to string.'''
        return str(m)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33.identity()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Identity matrix33
    def m33Ident():
        '''Identity matrix33.'''
        return pyrr.Matrix33.identity()

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns first column of matrix
    def m33c1(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns first column of matrix.'''
        return pyrr.Vector3(m.c1)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns second column of matrix
    def m33c2(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns second column of matrix.'''
        return pyrr.Vector3(m.c2)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns third column of matrix
    def m33c3(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns third column of matrix.'''
        return pyrr.Vector3(m.c3)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns first row of matrix
    def m33r1(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns first row of matrix.'''
        return pyrr.Vector3(m.r1)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns second row of matrix
    def m33r2(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns second row of matrix.'''
        return pyrr.Vector3(m.r2)

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns third row of matrix
    def m33r3(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns third row of matrix.'''
        return pyrr.Vector3(m.r3)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns a Quaternion representing this matrix
    def m33quat(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns a Quaternion representing this matrix.'''
        return m.quaternion

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns a Matrix44 representing this matrix
    def m33ToM44(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns a Matrix44 representing this matrix.'''
        return m.matrix44

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    ## Returns single scalar from matrix33. r and c taken as abs and clamped in range 1-3
    #  \param r: matrix row
    #  \param c: matrix column
    def m33GetComp(m=(DataTypes.Matrix33, pyrr.Matrix33()), r=(DataTypes.Int, 1), c=(DataTypes.Int, 1)):
        '''Returns single scalar from matrix33. r and c taken as abs and clamped in range 1-3.'''
        _r = clamp(abs(r), 1, 3)
        _c = clamp(abs(c), 1, 3)
        name = 'm{0}{1}'.format(_r, _c)
        return getattr(m, name)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33', 'quat']})
    ## Creates matrix33 from given quaternion
    def m33FromQuat(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Creates matrix33 from given quaternion.'''
        return pyrr.Matrix33(q)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33', '*']})
    ## Multiplies two m33 matrices m1 by m2
    def m33MultM33(m1=(DataTypes.Matrix33, pyrr.Matrix33()), m2=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Multiplies two m33 matrices m1 by m2.'''
        return m1 * m2

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33', '*']})
    def m33MultM44(m1=(DataTypes.Matrix33, pyrr.Matrix33()), m2=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Multiplies m33 by m44.\nm1 - m33\nm2 - m44.'''
        return m1 * m2

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33ApplyToV3(m=(DataTypes.Matrix33, pyrr.Matrix33()), v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''The matrix rotation are applied to the vector.\nReturns the vectors rotated by the specified matrix.'''
        return pyrr.Vector3(pyrr.matrix33.apply_to_vector(m, v))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33DirectionScale(v=(DataTypes.FloatVector3, pyrr.Vector3()), s=(DataTypes.Float, 0.0)):
        '''Creates a matrix which can apply a directional scaling to a set of vectors.\nAn example usage for this is to flatten a mesh against a single plane.\nReturns the scaling matrix.'''
        return pyrr.Matrix33(pyrr.matrix33.create_direction_scale(v, s))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromAxisAngle(axis=(DataTypes.FloatVector3, pyrr.Vector3()), theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix from the specified theta rotation around an axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_axis_rotation(axis, theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromEulers(eulers=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Creates a matrix from the specified Euler rotations.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_eulers(eulers))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['matrix33']})
    def m33FromInvOfQuat(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Creates a matrix with the inverse rotation of a quaternion.\nReturns a matrix with shape (3,3) that respresents the inverse of the quaternion.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_inverse_of_quaternion(q))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33From44(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Creates a Matrix33 from a Matrix44.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_matrix44(m))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromScale(s=(DataTypes.FloatVector3, pyrr.Vector3([1, 1, 1]))):
        '''Creates an identity matrix with the scale set.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_scale(s))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromX(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the X axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_x_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromY(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the Y axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_y_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33FromZ(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the Z axis.\ntheta in radians.'''
        return pyrr.Matrix33(pyrr.matrix33.create_from_z_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix33, pyrr.Matrix33()), meta={'Category': 'Math|Matrix33', 'Keywords': ['create', 'matrix33']})
    def m33Inverse(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Returns the inverse of the matrix.\nThis is essentially a wrapper around numpy.linalg.inv.'''
        return m.inverse
