# -*- coding: utf-8 -*-
## @brief Typical interfaces definition.
#
#Here we're just trying to make some typical interface definitions
#to better test the doxypypy filter.
#


from zope.interface import Interface, Attribute

# Public API Interfaces


## @brief     The zeroth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This is a special case commonly known as a "marker
#    interface" that declares neither methods nor attributes.
#
# @namespace sample_interfaces.INul
# @interface INul

class INul(Interface):

    pass


## @brief     The first sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has just a single method.
#
# @namespace sample_interfaces.IUnu
# @interface IUnu

class IUnu(Interface):

    pass

    ## @brief The first method offered for the first interface.
    # @namespace sample_interfaces.IUnu.unuMethod
    def unuMethod(unuArg, *args):

        pass


## @brief     The second sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has multiple methods.
#
# @namespace sample_interfaces.IDu
# @interface IDu

class IDu(Interface):

    pass

    ## @brief The first method offered for the second interface.
    # @namespace sample_interfaces.IDu.duMethod
    def duMethod(duArg1, duArg2):

        pass

    ## @brief The second method offered for the second interface.
    # @namespace sample_interfaces.IDu.duMethod2
    def duMethod2(duArg1, **kwargs):

        pass


## @brief     The third sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has just a single attribute.
#
# @namespace sample_interfaces.ITri
# @interface ITri

class ITri(Interface):

    pass

    ## @property triAttr
    # the first attribute for the third interface
    # @hideinitializer
    triAttr = Attribute('the first attribute for the third interface')


## @brief     The fourth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one has multiple attributes.
#
# @namespace sample_interfaces.IKvar
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


## @brief     The fifth sample interface.
#
#    Nothing special, just a sample interface to help test the
#    filter. This one opens things up a little and has multiple
#    attributes and methods.
#
# @namespace sample_interfaces.IKvin
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

    ## @brief The first method offered for the fifth interface.
    # @namespace sample_interfaces.IKvin.kvinMethod
    def kvinMethod(kvinArg1, kvinArg2, *args, **kwargs):

        pass

    ## @brief The second method offered for the fifth interface.
    # @namespace sample_interfaces.IKvin.kvinMethod2
    def kvinMethod2(kvinArg1, kvinArg2='default'):

        pass

    ## @property kvinAttr3
    # the third attribute for the fifth interface
    # @hideinitializer
    kvinAttr3 = Attribute('the third attribute for the fifth interface')

    ## @brief The third method offered for the fifth interface.
    # @namespace sample_interfaces.IKvin.kvinMethod3
    def kvinMethod3(kvinArg1, kvinArg2='default'):

        pass
