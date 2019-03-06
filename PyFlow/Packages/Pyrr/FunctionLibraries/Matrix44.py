import pyrr

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.AGraphCommon import *
from PyFlow.Packages.Pyrr import PACKAGE_NAME


class Matrix44(FunctionLibraryBase):
    packageName = PACKAGE_NAME
    '''doc string for Matrix44'''
    def __init__(self):
        super(Matrix44, self).__init__()

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Matrix44', 'Keywords': []})
    def m44Zero():
        '''zero matrix44'''
        return pyrr.Matrix44()

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', str(pyrr.Matrix44())), meta={'Category': 'Math|Matrix44', 'Keywords': []})
    def m44ToStr(m=('Matrix44Pin', pyrr.Matrix44())):
        '''M44 to string.'''
        return str(m)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44.identity()), nodeType=NodeTypes.Pure, meta={'Category': 'Math|Matrix44', 'Keywords': []})
    def m44Ident():
        '''Identity matrix44.'''
        return pyrr.Matrix44.identity()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector3Pin', pyrr.Vector3()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44ApplyToV3(m=('Matrix44Pin', pyrr.Matrix44()), v=('FloatVector3Pin', pyrr.Vector3())):
        '''Apply a matrix to a vector.\nThe matrix rotation and translation are applied to the vector. '''
        return pyrr.Vector3(pyrr.matrix44.apply_to_vector(m, v))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromAxisAngle(axis=('FloatVector3Pin', pyrr.Vector3()), theta=('FloatPin', 0.0)):
        '''Creates a matrix from the specified theta rotation around an axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_axis_rotation(axis, theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromX(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the X axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_x_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromY(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the Y axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_y_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromZ(theta=('FloatPin', 0.0)):
        '''Creates a matrix with the specified rotation about the Z axis.\ntheta in radians.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_z_rotation(theta))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromEulers(eulers=('FloatVector3Pin', pyrr.Vector3())):
        '''Creates a matrix from the specified Euler rotations.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_eulers(eulers))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44FromInvOfQuat(q=('QuatPin', pyrr.Quaternion())):
        '''Creates a matrix with the inverse rotation of a quaternion.\nReturns a matrix with shape (4,4) that respresents the inverse of the quaternion.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_inverse_of_quaternion(q))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44From33(m=('Matrix33Pin', pyrr.Matrix33())):
        '''Creates a Matrix44 from a Matrix33.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_matrix33(m))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44', 'quat']})
    def m44FromQuat(q=('QuatPin', pyrr.Quaternion())):
        '''Creates matrix44 from given quaternion.'''
        return pyrr.Matrix44(q)

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromScale(s=('FloatVector3Pin', pyrr.Vector3([1, 1, 1]))):
        '''Creates an identity matrix with the scale set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_scale(s))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromTransV3(t=('FloatVector3Pin', pyrr.Vector3())):
        '''Creates an identity matrix with the translation set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_translation(t))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44FromTransV4(t=('FloatVector4Pin', pyrr.Vector4())):
        '''Creates an identity matrix with the translation set.'''
        return pyrr.Matrix44(pyrr.matrix44.create_from_translation(t))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44LookAtCreate(eye=('FloatVector3Pin', pyrr.Vector3()), target=('FloatVector3Pin', pyrr.Vector3()), up=('FloatVector3Pin', pyrr.Vector3())):
        '''Creates a look at matrix according to OpenGL standards.\nReturns a look at matrix that can be used as a viewMatrix.'''
        return pyrr.Matrix44(pyrr.matrix44.create_look_at(eye, target, up))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m33ViewCreate(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns a view into the matrix in Matrix33 format.\nThis is different from m33From44, in that changes to the returned matrix will also alter the original matrix.'''
        return pyrr.Matrix44(pyrr.matrix44.create_matrix33_view(m))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44OrthoProj(left=('FloatPin', -5.0), right=('FloatPin', 5.0), bottom=('FloatPin', -5.0), top=('FloatPin', 5.0), near=('FloatPin', 0.0), far=('FloatPin', 10.0), result=("Reference", ('BoolPin', False))):
        '''Creates an orthogonal projection matrix.\n\nleft (float) - The left of the near plane relative to the planes centre.\n\nright (float) - The right of the near plane relative to the planes centre.\n\ntop (float) - The top of the near plane relative to the planes centre.\n\nbottom (float) - The bottom of the near plane relative to the planes centre.\n\nnear (float) - The distance of the near plane from the cameras origin. It is recommended that the near plane is set to 1.0 or above to avoid rendering issues at close range.\n\nfar (float) - The distance of the far plane from the cameras origin.'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_orthogonal_projection(left, right, bottom, top, near, far))
            result(True)
            return m
        except:
            result(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44PerspProj(fovy=('FloatPin', 0.0), aspect=('FloatPin', 0.0), near=('FloatPin', 0.0), far=('FloatPin', 0.0)):
        '''Creates perspective projection matrix.\n\nfovy (float) - field of view in y direction in degrees\n\naspect (float) - aspect ratio of the view (width / height)\n\nnear (float) - distance from the viewer to the near clipping plane (only positive)\n\nfar (float) - distance from the viewer to the far clipping plane (only positive).'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_perspective_projection(fovy, aspect, near, far))
            result(True)
            return m
        except:
            result(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44PerspProjBounds(left=('FloatPin', -5.0), right=('FloatPin', 5.0), bottom=('FloatPin', -5.0), top=('FloatPin', 5.0), near=('FloatPin', 0.0), far=('FloatPin', 10.0), result=("Reference", ('BoolPin', False))):
        '''Creates a perspective projection matrix using the specified near plane dimensions.\n\nleft (float) - The left of the near plane relative to the planes centre.\n\nright (float) - The right of the near plane relative to the planes centre.\n\ntop (float) - The top of the near plane relative to the planes centre.\n\nbottom (float) - The bottom of the near plane relative to the planes centre.\n\nnear (float) - The distance of the near plane from the cameras origin. It is recommended that the near plane is set to 1.0 or above to avoid rendering issues at close range.\n\nfar (float) - The distance of the far plane from the cameras origin.'''
        try:
            m = pyrr.Matrix44(pyrr.matrix44.create_perspective_projection_from_bounds(left, right, bottom, top, near, far))
            result(True)
            return m
        except:
            result(False)
            return pyrr.Matrix44.identity()

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44Decompose(m=('Matrix44Pin', pyrr.Matrix44()), t=("Reference", ('FloatVector3Pin', pyrr.Vector3())), r=("Reference", ('QuatPin', pyrr.Quaternion())), s=("Reference", ('FloatVector3Pin', pyrr.Vector3()))):
        '''Decomposes an affine transformation matrix into its scale, rotation and translation components.'''
        _s, _r, _t = pyrr.matrix44.decompose(m)
        t(pyrr.Vector3(_t))
        r(pyrr.Quaternion(_r))
        s(pyrr.Vector3(_s))

    @staticmethod
    @IMPLEMENT_NODE(returns=('Matrix44Pin', pyrr.Matrix44()), meta={'Category': 'Math|Matrix44', 'Keywords': ['create', 'matrix44']})
    def m44Inverse(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns the inverse of the matrix.\nThis is essentially a wrapper around numpy.linalg.inv.'''
        return ~m

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c1(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns first column of matrix.'''
        return pyrr.Vector4(m.c1.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c2(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns second column of matrix.'''
        return pyrr.Vector4(m.c2.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c3(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns third column of matrix.'''
        return pyrr.Vector4(m.c3.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44c4(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns fourth column of matrix.'''
        return pyrr.Vector4(m.c4.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r1(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns first row of matrix.'''
        return pyrr.Vector4(m.r1.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r2(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns second row of matrix.'''
        return pyrr.Vector4(m.r2.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r3(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns third row of matrix.'''
        return pyrr.Vector4(m.r3.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatVector4Pin', pyrr.Vector4()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44r4(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns fourth row of matrix.'''
        return pyrr.Vector4(m.r4.tolist())

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', 0.0), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44GetComp(m=('Matrix44Pin', pyrr.Matrix44()), r=('IntPin', 1), c=('IntPin', 1)):
        '''Returns single scalar from matrix44. r and c taken as abs and clamped in range 1-4.'''
        _r = clamp(abs(r), 1, 4)
        _c = clamp(abs(c), 1, 4)
        name = 'm{0}{1}'.format(_r, _c)
        return getattr(m, name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('QuatPin', pyrr.Quaternion()), meta={'Category': 'Math|Matrix44', 'Keywords': ['matrix44']})
    def m44quat(m=('Matrix44Pin', pyrr.Matrix44())):
        '''Returns a Quaternion representing this matrix.'''
        return m.quaternion
