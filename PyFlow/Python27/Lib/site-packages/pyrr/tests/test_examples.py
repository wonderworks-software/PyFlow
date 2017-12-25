from __future__ import absolute_import
try:
    import unittest2 as unittest
except:
    import unittest


class test_procedural_examples(unittest.TestCase):
    def test_procedural_examples(self):
        from pyrr import quaternion, matrix44, vector3
        import numpy as np

        point = vector3.create(1.,2.,3.)
        orientation = quaternion.create()
        translation = vector3.create()
        scale = vector3.create(1,1,1)

        # translate along X by 1
        translation += [1.0, 0.0, 0.0]

        # rotate about Y by pi/2
        rotation = quaternion.create_from_y_rotation(np.pi / 2.0)
        orientation = quaternion.cross(rotation, orientation)

        # create a matrix
        # start our matrix off using the scale
        matrix = matrix44.create_from_scale(scale)

        # apply our orientation
        orientation = matrix44.create_from_quaternion(orientation)
        matrix = matrix44.multiply(matrix, orientation)

        # apply our translation
        translation_matrix = matrix44.create_from_translation(translation)
        matrix = matrix44.multiply(matrix, translation_matrix)

        # transform our point by the matrix
        point = matrix44.apply_to_vector(matrix, point)
