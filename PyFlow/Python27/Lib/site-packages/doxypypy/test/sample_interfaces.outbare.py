# -*- coding: utf-8 -*-
##
#Typical interfaces definition.
#
#Here we're just trying to make some typical interface definitions
#to better test the doxypypy filter.
#

from zope.interface import Interface, Attribute

# Public API Interfaces


##
#    The zeroth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This is a special case commonly known as a "marker
#    interface" that declares neither methods nor attributes.
#
#
# @interface INul
class INul(Interface):

    pass


##
#    The first sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has just a single method.
#
#
# @interface IUnu
class IUnu(Interface):

    pass

    ##The first method offered for the first interface.
    def unuMethod(unuArg, *args):

        pass


##
#    The second sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has multiple methods.
#
#
# @interface IDu
class IDu(Interface):

    pass

    ##The first method offered for the second interface.
    def duMethod(duArg1, duArg2):

        pass

    ##The second method offered for the second interface.
    def duMethod2(duArg1, **kwargs):

        pass


##
#    The third sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has just a single attribute.
#
#
# @interface ITri
class ITri(Interface):

    pass

    ## @property triAttr
    # the first attribute for the third interface
    # @hideinitializer
    triAttr = Attribute('the first attribute for the third interface')


##
#    The fourth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has multiple attributes.
#
#
# @interface IKvar
class IKvar(Interface):

    pass

    ## @property kvarAttr1
    # the first attribute for the fourth interface
    # @hideinitializer
    kvarAttr1 = Attribute('the first attribute for the fourth interface')

    ## @property kvarAttr2
    # the second attribute for the fourth interface
    # @hideinitializer
    kvarAttr2 = Attribute('the second attribute for the fourth interface')


##
#    The fifth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one opens things up a little and has multiple
#    attributes and methods.
#
#
# @interface IKvin
class IKvin(Interface):

    pass

    ## @property kvinAttr1
    # the first attribute for the fifth interface
    # @hideinitializer
    kvinAttr1 = Attribute('the first attribute for the fifth interface')

    ## @property kvinAttr2
    # the second attribute for the fifth interface
    # @hideinitializer
    kvinAttr2 = Attribute('the second attribute for the fifth interface')

    ##The first method offered for the fifth interface.
    def kvinMethod(kvinArg1, kvinArg2, *args, **kwargs):

        pass

    ##The second method offered for the fifth interface.
    def kvinMethod2(kvinArg1, kvinArg2='default'):

        pass

    ## @property kvinAttr3
    # the third attribute for the fifth interface
    # @hideinitializer
    kvinAttr3 = Attribute('the third attribute for the fifth interface')

    ##The third method offered for the fifth interface.
    def kvinMethod3(kvinArg1, kvinArg2='default'):

        pass
