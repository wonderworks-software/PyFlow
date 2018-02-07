# -*- coding: utf-8 -*-
"""
Typical interfaces definition.

Here we're just trying to make some typical interface definitions
to better test the doxypypy filter.
"""

from zope.interface import Interface, Attribute

# Public API Interfaces


class INul(Interface):
    """
    The zeroth sample interface.

    Nothing special, just a sample interface to help test the
    filter. This is a special case commonly known as a "marker
    interface" that declares neither methods nor attributes.
    """


class IUnu(Interface):
    """
    The first sample interface.

    Nothing special, just a sample interface to help test the
    filter. This one has just a single method.
    """

    def unuMethod(unuArg, *args):
        """The first method offered for the first interface."""


class IDu(Interface):
    """
    The second sample interface.

    Nothing special, just a sample interface to help test the
    filter. This one has multiple methods.
    """

    def duMethod(duArg1, duArg2):
        """The first method offered for the second interface."""

    def duMethod2(duArg1, **kwargs):
        """The second method offered for the second interface."""


class ITri(Interface):
    """
    The third sample interface.

    Nothing special, just a sample interface to help test the
    filter. This one has just a single attribute.
    """

    triAttr = Attribute('the first attribute for the third interface')


class IKvar(Interface):
    """
    The fourth sample interface.

    Nothing special, just a sample interface to help test the
    filter. This one has multiple attributes.
    """

    kvarAttr1 = Attribute('the first attribute for the fourth interface')

    kvarAttr2 = Attribute('the second attribute for the fourth interface')


class IKvin(Interface):
    """
    The fifth sample interface.

    Nothing special, just a sample interface to help test the
    filter. This one opens things up a little and has multiple
    attributes and methods.
    """

    kvinAttr1 = Attribute('the first attribute for the fifth interface')

    kvinAttr2 = Attribute('the second attribute for the fifth interface')

    def kvinMethod(kvinArg1, kvinArg2, *args, **kwargs):
        """The first method offered for the fifth interface."""

    def kvinMethod2(kvinArg1, kvinArg2='default'):
        """The second method offered for the fifth interface."""

    kvinAttr3 = Attribute('the third attribute for the fifth interface')

    def kvinMethod3(kvinArg1, kvinArg2='default'):
        """The third method offered for the fifth interface."""
