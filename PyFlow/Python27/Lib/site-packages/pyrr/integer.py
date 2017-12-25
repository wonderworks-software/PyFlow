# -*- coding: utf-8 -*-
"""Provide functions for the manipulation of integers.
"""

def count_bits(value):
    """Counts the number of bits set to 1 in an integer.

    For example::

        >>> count_bits(0b101111)
        5
        >>> count_bits(0xf)
        4
        >>> count_bits(8)
        1
        >>> count_bits(3)
        2
    
    :param int value: An integer.
    :rtype: integer
    :return: The count of bits set to 1.

    .. seealso:: http://wiki.python.org/moin/BitManipulation
    """
    count = 0
    while (value):
        count += (value & 1)
        value >>= 1
    
    return count

