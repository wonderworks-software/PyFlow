# -*- coding: utf-8 -*-
"""Provide functions for the trigonometric functions.
"""
from __future__ import absolute_import, division, print_function
import math


def aspect_ratio(width, height):
    return float(width) / float(height)

def calculate_fov(zoom, height=1.0):
    """Calculates the required FOV to set the
    view frustrum to have a view with the specified height
    at the specified distance.

    :param float zoom: The distance to calculate the FOV for.
    :param float height: The desired view height at the specified
        distance.
        The default is 1.0.
    :rtype: A float representing the FOV to use in degrees.
    """
    # http://www.glprogramming.com/red/chapter03.html
    rad_theta = 2.0 * math.atan2(height / 2.0, zoom)
    return math.degrees(rad_theta)

def calculate_zoom(fov, height=1.0):
    """Calculates the zoom (distance) from the camera
    with the specified FOV and height of image.

    :param float fov: The FOV to use.
    :param float height: The height of the image at the
        desired distance.
    :rtype: A float representing the zoom (distance) from the camera for the
        desired height at the specified FOV.
    :raise ZeroDivisionError: Raised if the fov is
        0.0.
    """
    return float(height) / math.tan(fov / 2.0)

def calculate_height(fov, zoom):
    """Performs the opposite of calculate_fov.
    Used to find the current height at a specific distance.

    :param float fov: The current FOV.
    :param float zoom: The distance to calculate the height
        for.
    :rtype: A float representing the height at the specified distance for the
        specified FOV.
    """
    height = zoom * (math.tan(fov / 2.0))
    return height

def calculate_plane_size(aspect_ratio, fov, distance):
    """Calculates the width and height of a plane at the
    specified distance using the FOV of the frustrum
    and aspect ratio of the viewport.

    :param float aspect_ratio: The aspect ratio of the viewport.
    :param float fov: The FOV of the frustrum.
    :param float distance: The distance from the origin/camera
        of the plane to calculate.
    :rtype: A tuple of two floats: width and height: The width and height of
        the plane.
    """
    # http://www.songho.ca/opengl/gl_transform.html
    # http://nehe.gamedev.net/article/replacement_for_gluperspective/21002/
    # http://steinsoft.net/index.php?site=Programming/Code%20Snippets/OpenGL/gluperspective&printable=1
    tangent = math.radians(fov)
    height = distance * tangent
    width = height * aspect_ratio

    return width * 2.0, height * 2.0

