# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of 2D Rectangles.

Rectangles are represented using a numpy.array of shape (2,2,).

The first value is a vector of x, y position of the rectangle.
The second value is a vector with the width, height of the rectangle.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the position vector within the rectangle
    position = 0

    #: The index of the size vector within the rectangle
    size = 1


def create(x=0., y=0., width=1., height=1., dtype=None):
    """Creates a rectangle from the specified position and sizes.

    This function will interpret the values literally. A negative width
    or height will be represented by the returned value.

    :rtype: numpy.array
    :return: Returns a rectangle with the specified values.
    """
    return np.array([[x, y], [width, height]], dtype=dtype)

def create_zeros(dtype=None):
    return np.zeros((2,2), dtype=dtype)

def create_from_bounds(left, right, bottom, top, dtype=None):
    """Creates a rectangle from the specified boundaries.

    This caters for the left and right, and for the
    top and bottom being swapped.

    :rtype: numpy.array
    :return: Returns a rectangle with the specified values.
        The rectangle will have a positive width and height
        regardless of the values passed in.
    """
    xmin = min(left, right)
    xmax = max(left, right)
    ymin = min(top, bottom)
    ymax = max(top, bottom)

    return create(
        xmin,
        ymin,
        xmax - xmin,
        ymax - ymin,
        dtype
    )

@all_parameters_as_numpy_arrays
def bounds(rect):
    """Returns the absolute boundaries of the rectangle.

    This caters for rectangles with a negative width.

    :rtype: Tuple of 4 floats
    :return: The absolute left, right, bottom and top of the rectangle.
    """
    left = rect[0,0]
    right = rect[0,0] + rect[1,0]
    top = rect[0,1]
    bottom = rect[0,1] + rect[1,1]

    xmin = min(left, right)
    xmax = max(left, right)
    ymin = min(top, bottom)
    ymax = max(top, bottom)

    return xmin, xmax, ymin, ymax

@all_parameters_as_numpy_arrays
def position(rect):
    """Returns the literal position of the rectangle.

    This is the bottom-left point of the rectangle for
    rectangles with positive width and height

    :rtype: numpy.array
    :return: The position of the rectangle.
    """
    return rect[0].copy()

@all_parameters_as_numpy_arrays
def size(rect):
    """Returns the literal size of the rectangle.

    These values may be negative.

    :rtype: numpy.array
    :return: The size of the rectangle.
    """
    return rect[1].copy()

def abs_size(rect):
    """Returns the absolute size of the rectangle.

    :rtype: numpy.array
    :return: The absolute size of the rectangle.
    """
    return np.absolute(rect[1])

def x(rect):
    """Returns the X position of the rectangle.

    This will be the left for rectangles with positive height values.

    :rtype: float
    :return: The X position of the rectangle. This value
        will be further right than the 'right' if the width is negative.
    """
    return rect[0][0]

def y(rect):
    """Returns the Y position of the rectangle.

    This will be the bottom for rectangles with positive height values.

    :rtype: float
    :return: The Y position of the rectangle. This value
        will be above the bottom if the height is negative.
    """
    return rect[0][1]

def width(rect):
    """Returns the literal width of the rectangle.

    :rtype: float
    :return: The width of the rectangle. This can be a
        negative value.
    """
    return rect[1][0]

def abs_width(rect):
    """Returns the absolute width of the rectangle.

    This caters for rectangles with a negative width.

    :rtype: float
    :return: The absolute width of the rectangle.
    """
    return abs(width(rect))

def height(rect):
    """Returns the literal height of the rectangle.

    :rtype: float
    :return: The height of the rectangle. This can be a
        negative value.
    """
    return rect[1][1]

def abs_height(rect):
    """Returns the absolute height of the rectangle.

    This caters for rectangles with a negative height.

    :rtype: float
    :return: The absolute height of the rectangle.
    """
    return abs(height(rect))

def top(rect):
    """Returns the top most Y value of the rectangle.

    This caters for rectangles with a negative height.

    :rtype: float
    :return: The biggest Y value.
    """
    return max(
        rect[0][1],
        rect[0][1] + rect[1][1]
       )

def bottom(rect):
    """Returns the bottom most Y value of the rectangle.

    This caters for rectangles with a negative height.

    :rtype: float
    :return: The smallest Y value.
    """
    return min(
        rect[0][1],
        rect[0][1] + rect[1][1]
       )

def left(rect):
    """Returns the left most X value of the rectangle.

    This caters for rectangles with a negative width.

    :rtype: float
    :return: The smallest X value.
    """
    return min(
        rect[0][0],
        rect[0][0] + rect[1][0]
       )

def right(rect):
    """Returns the right most X value of the rectangle.

    This caters for rectangles with a negative width.

    :rtype: float
    :return: The biggest X value.
    """
    return max(
        rect[0][0],
        rect[0][0] + rect[1][0]
       )

@parameters_as_numpy_arrays('rect')
def scale_by_vector(rect, vec):
    """Scales a rectangle by a 2D vector.

    Note that this will also scale the X,Y
    value of the rectangle, which will cause
    the rectangle to move, not just increase
    in size.

    :param numpy.array rect: the rectangle to scale.
        Both x,y and width,height will be scaled.
    :param vec: A 2D vector to scale the rect by.
    :rtype: numpy.array.
    """
    return rect * vec[:2]

def aspect_ratio(rect):
    width = float(abs_width(rect))
    height = float(abs_height(rect))
    return width / height


