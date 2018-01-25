from FunctionLibrary import *
from AGraphCommon import *
import pyrr


class QuatLib(FunctionLibraryBase):
    '''doc string for QuatLib'''
    def __init__(self):
        super(QuatLib, self).__init__()

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def zeroQuat():
        '''zero quaternion'''
        return pyrr.Quaternion()

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromXRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the X-axis.'''
        return pyrr.Quaternion.from_x_rotation(theta)

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromYRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the X-axis.'''
        return pyrr.Quaternion.from_y_rotation(theta)

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromZRotation(theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the X-axis.'''
        return pyrr.Quaternion.from_z_rotation(theta)

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromMatrix33(m=(DataTypes.Matrix33, pyrr.Matrix33())):
        '''Creates a Quaternion from the specified Matrix33.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromMatrix44(m=(DataTypes.Matrix44, pyrr.Matrix44())):
        '''Creates a Quaternion from the specified Matrix33.'''
        return pyrr.Quaternion.from_matrix(m)

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromEulers(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_eulers([a, b, c])

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromInverseOfEulers(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0)):
        '''Creates a Quaternion from the specified Euler angles.'''
        return pyrr.Quaternion.from_inverse_of_eulers([a, b, c])

    @staticmethod
    @annotated(returns=DataTypes.Quaternion, nodeType=NodeTypes.Pure, meta={'Category': 'pyrr|Quaternion', 'Keywords': []})
    def quatFromAxisRotation(a=(DataTypes.Float, 0.0), b=(DataTypes.Float, 0.0), c=(DataTypes.Float, 0.0), theta=(DataTypes.Float, 0.0)):
        '''Creates a new Quaternion with a rotation around the specified axis.'''
        return pyrr.Quaternion.from_axis_rotation([a, b, c], theta)
