# -*- coding: utf-8 -*-
from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class Matrix44(FunctionLibraryBase):
    '''doc string for Matrix44'''
    def __init__(self):
        super(Matrix44, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix44', 'Keywords': []})
    def m44Zero():
        '''zero matrix44'''
        return pyrr.Matrix44()

    @staticmethod
    @implementNode(returns=(DataTypes.String, str(pyrr.Matrix44())), meta={'Category': 'Math|Matrix44', 'Keywords': []})
    def m44ToStr(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''M44 to string.'''
        return str(m)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44.identity()), nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Matrix44', 'Keywords': []})
    def m44Ident():
        '''Identity matrix44.'''
        return pyrr.Matrix44.identity()

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector3, pyrr.Vector3()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44ApplyToV3(m=(DataTypes.Matrix44, pyrr.Matrix44()), v=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Apply a matrix to a vector.\nThe matrix rotation and translation are applied to the vector. '''
        return pyrr.Vector3(pyrr.matrix44.apply_to_vector(m, v))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromAxisAngle(axis=(DataTypes.FloatVector3, pyrr.Vector3()), theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix from the specified theta rotation around an axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_axis_rotation(axis, theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromX(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the X axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_x_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromY(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the Y axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_y_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromZ(theta=(DataTypes.Float, 0.0)):
        '''Creates a matrix with the specified rotation about the Z axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_z_rotation(theta))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromEulers(eulers=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Creates a matrix from the specified Euler rotations.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_eulers(eulers))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromInvOfQuat(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Creates a matrix with the inverse rotation of a quaternion.\nReturns a matrix with shape (4,4) that respresents the inverse of the quaternion.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_inverse_of_quaternion(q))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44From33(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Creates a Matrix44 from a Matrix33.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_matrix33(m))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44', 'quat']})
    def m44FromQuat(q=(DataTypes.Quaternion, pyrr.Quaternion())):
        '''Creates matrix44 from given quaternion.'''
        return pyrr.Matrix44(q)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromScale(s=(DataTypes.FloatVector3, pyrr.Vector3([1, 1, 1]))):
        '''Creates an identity matrix with the scale set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_scale(s))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromTransV3(t=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Creates an identity matrix with the translation set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_translation(t))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromTransV4(t=(DataTypes.FloatVector4, pyrr.Vector4())):
        '''Creates an identity matrix with the translation set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_translation(t))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44LookAtCreate(eye=(DataTypes.FloatVector3, pyrr.Vector3()), target=(DataTypes.FloatVector3, pyrr.Vector3()), up=(DataTypes.FloatVector3, pyrr.Vector3())):
        '''Creates a look at matrix according to OpenGL standards.\nReturns a look at matrix that can be used as a viewMatrix.'''
        return pyrr.Matrix44(pyrr.matrix44.create_look_at(eye, target, up))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m33ViewCreate(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns a view into the matrix in Matrix33 format.\nThis is different from m33From44, in that changes to the returned matrix will also alter the original matrix.'''
        return pyrr.Matrix44(pyrr.matrix44.create_matrix33_view(m))

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44OrthoProj(left=(DataTypes.Float, -5.0), right=(DataTypes.Float, 5.0), bottom=(DataTypes.Float, -5.0), top=(DataTypes.Float, 5.0), near=(DataTypes.Float, 0.0), far=(DataTypes.Float, 10.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Creates an orthogonal projection matrix.\n\nleft (float) - The left of the near plane relative to the planes centre.\n\nright (float) - The right of the near plane relative to the planes centre.\n\ntop (float) - The top of the near plane relative to the planes centre.\n\nbottom (float) - The bottom of the near plane relative to the planes centre.\n\nnear (float) - The distance of the near plane from the cameras origin. It is recommended that the near plane is set to 1.0 or above to avoid rendering issues at close range.\n\nfar (float) - The distance of the far plane from the cameras origin.'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_orthogonal_projection(left, right, bottom, top, near, far))
            result.setData(True)
            return m
        except:
            result.setData(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44PerspProj(fovy=(DataTypes.Float, 0.0), aspect=(DataTypes.Float, 0.0), near=(DataTypes.Float, 0.0), far=(DataTypes.Float, 0.0)):
        '''Creates perspective projection matrix.\n\nfovy (float) - field of view in y direction in degrees\n\naspect (float) - aspect ratio of the view (width / height)\n\nnear (float) - distance from the viewer to the near clipping plane (only positive)\n\nfar (float) - distance from the viewer to the far clipping plane (only positive).'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_perspective_projection(fovy, aspect, near, far))
            result.setData(True)
            return m
        except:
            result.setData(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44PerspProjBounds(left=(DataTypes.Float, -5.0), right=(DataTypes.Float, 5.0), bottom=(DataTypes.Float, -5.0), top=(DataTypes.Float, 5.0), near=(DataTypes.Float, 0.0), far=(DataTypes.Float, 10.0), result=(DataTypes.Reference, DataTypes.Bool)):
        '''Creates a perspective projection matrix using the specified near plane dimensions.\n\nleft (float) - The left of the near plane relative to the planes centre.\n\nright (float) - The right of the near plane relative to the planes centre.\n\ntop (float) - The top of the near plane relative to the planes centre.\n\nbottom (float) - The bottom of the near plane relative to the planes centre.\n\nnear (float) - The distance of the near plane from the cameras origin. It is recommended that the near plane is set to 1.0 or above to avoid rendering issues at close range.\n\nfar (float) - The distance of the far plane from the cameras origin.'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_perspective_projection_from_bounds(left, right, bottom, top, near, far))
            result.setData(True)
            return m
        except:
            result.setData(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @implementNode(returns=None, meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44Decompose(m=(DataTypes.Matrix44, pyrr.Matrix44()), s=(DataTypes.Reference, DataTypes.FloatVector3), r=(DataTypes.Reference, DataTypes.Quaternion), t=(DataTypes.Reference, DataTypes.FloatVector3)):
        '''Decomposes an affine transformation matrix into its scale, rotation and translation components.'''
        _s, _r, _t = pyrr.matrix44.decompose(m)
        s.setData(_s)
        r.setData(_r)
        t.setData(_t)

    @staticmethod
    @implementNode(returns=(DataTypes.Matrix44, pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44Inverse(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns the inverse of the matrix.\nThis is essentially a wrapper around numpy.linalg.inv.'''
        return ~m

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c1(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns first column of matrix.'''
        return pyrr.Vector4(m.c1.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c2(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns second column of matrix.'''
        return pyrr.Vector4(m.c2.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c3(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns third column of matrix.'''
        return pyrr.Vector4(m.c3.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c4(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns fourth column of matrix.'''
        return pyrr.Vector4(m.c4.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r1(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns first row of matrix.'''
        return pyrr.Vector4(m.r1.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r2(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns second row of matrix.'''
        return pyrr.Vector4(m.r2.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r3(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns third row of matrix.'''
        return pyrr.Vector4(m.r3.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.FloatVector4, pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r4(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns fourth row of matrix.'''
        return pyrr.Vector4(m.r4.tolist())

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44GetComp(m=(DataTypes.Matrix44, pyrr.Matrix44()), r=(DataTypes.Int, 1), c=(DataTypes.Int, 1)):
        '''Returns single scalar from matrix44. r and c taken as abs and clamped in range 1-4.'''
        _r = clamp(abs(r), 1, 4)
        _c = clamp(abs(c), 1, 4)
        name = 'm{0}{1}'.format(_r, _c)
        return getattr(m, name)

    @staticmethod
    @implementNode(returns=(DataTypes.Quaternion, pyrr.Quaternion()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44quat(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Returns a Quaternion representing this matrix.'''
        return m.quaternion
