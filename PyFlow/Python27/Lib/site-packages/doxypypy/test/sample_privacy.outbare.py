# -*- coding: utf-8 -*-
##
#Typical class with private members.
#
#Here we're just trying to make a fairly straightforward class
#that has some private (Python-enforced private, name-mangled)
#and protected (by convention only, a.k.a. "bed lump")
#variables.
#
__notPrivateModuleAttr__ = 1
## @var __privateModuleAttr
# @hideinitializer
# @private
__privateModuleAttr = 2
## @var _protectedModuleAttr
# @hideinitializer
# @protected
_protectedModuleAttr = 3


##
#    A sample new-style class.
#
#    Nothing special, just a basic new-style class that has some
#    private and protected members in it.
#
class NewStyleSample(object):
    __notPrivateClassAttr__ = 1
    ## @var __privateClassAttr
    # @hideinitializer
    # @private
    __privateClassAttr = 2
    ## @var _protectedClassAttr
    # @hideinitializer
    # @protected
    _protectedClassAttr = 3

    ##
    #        This constructor won't be private.
    #
    def __init__(self):
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    ##
    #        This will be not be private.
    #
    def __notPrivateClassMethod__(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be private.
    #
    #
    # @private
    def __privateClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be protected.
    #
    #
    # @protected
    def _protectedClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be public.
    #
    def publicClassMethod(self):
        public = 0
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.public = public
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This static method will be public.
    #
    @staticmethod
    def publicClassStaticMethod():
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This class method will be public.
    #
    @classmethod
    def publicClassClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        An inner not private class.
    #
    #        Nothing special, just a not private helper class.
    #
    class __innerNotPrivate__(object):
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ##
    #        An inner protected class.
    #
    #        Nothing special, just a protected helper class.
    #
    #
    # @private
    class __innerProtected(object):
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ##
    #        An inner private class.
    #
    #        Nothing special, just a private helper class.
    #
    #
    # @private
    class __innerPrivate(object):
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


##
#    A sample old-style class.
#
#    Nothing special, just a basic old-style class that has some
#    private and protected members in it.
#
class OldStyleSample():
    __notPrivateClassAttr__ = 1
    ## @var __privateClassAttr
    # @hideinitializer
    # @private
    __privateClassAttr = 2
    ## @var _protectedClassAttr
    # @hideinitializer
    # @protected
    _protectedClassAttr = 3

    ##
    #        This constructor won't be private.
    #
    def __init__(self):
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    ##
    #        This will be not be private.
    #
    def __notPrivateClassMethod__(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be private.
    #
    #
    # @private
    def __privateClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be protected.
    #
    #
    # @protected
    def _protectedClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This will be public.
    #
    def publicClassMethod(self):
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    ##
    #        This static method will be public.
    #
    @staticmethod
    def publicClassStaticMethod():
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This class method will be public.
    #
    @classmethod
    def publicClassClassMethod(self):
        public = 0
        __notPrivateAttr__ = 1
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = 2
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = 3
        self.public = public
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        An inner not private class.
    #
    #        Nothing special, just a not private helper class.
    #
    class __innerNotPrivate__():
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ##
    #        An inner protected class.
    #
    #        Nothing special, just a protected helper class.
    #
    #
    # @private
    class __innerProtected():
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ##
    #        An inner private class.
    #
    #        Nothing special, just a private helper class.
    #
    #
    # @private
    class __innerPrivate():
        ##
        #            This constructor won't be private.
        #
        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


##
#    A sample function.
#
#    Nothing special, just a basic function that has some private
#    and protected variables in it.
#
def Function():
    __notPrivateFunctionAttr__ = 1
    ## @var __privateFunctionAttr
    # @hideinitializer
    # @private
    __privateFunctionAttr = 2
    ## @var _protectedFunctionAttr
    # @hideinitializer
    # @protected
    _protectedFunctionAttr = 3

    ##
    #        This will not be private.
    #
    def __notPrivateFunction__():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be private.
    #
    #
    # @private
    def __privateNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be protected.
    #
    #
    # @protected
    def _protectedNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be public.
    #
    def publicNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction


##
#    A sample protected function.
#
#    Nothing special, just a basic protected function that has some
#    private and protected variables in it.
#
#
# @protected
def _ProtectedFunction():
    __notPrivateFunctionAttr__ = 1
    ## @var __privateFunctionAttr
    # @hideinitializer
    # @private
    __privateFunctionAttr = 2
    ## @var _protectedFunctionAttr
    # @hideinitializer
    # @protected
    _protectedFunctionAttr = 3

    ##
    #        This will not be private.
    #
    def __notPrivateFunction__():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be private.
    #
    #
    # @private
    def __privateNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be protected.
    #
    #
    # @protected
    def _protectedNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be public.
    #
    def publicNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction


##
#    A sample private function.
#
#    Nothing special, just a basic private function that has some
#    private and protected variables in it.
#
#
# @private
def __PrivateFunction():
    __notPrivateFunctionAttr__ = 1
    ## @var __privateFunctionAttr
    # @hideinitializer
    # @private
    __privateFunctionAttr = 2
    ## @var _protectedFunctionAttr
    # @hideinitializer
    # @protected
    _protectedFunctionAttr = 3

    ##
    #        This will not be private.
    #
    def __notPrivateFunction__():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be private.
    #
    #
    # @private
    def __privateNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be protected.
    #
    #
    # @protected
    def _protectedNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    ##
    #        This will be public.
    #
    def publicNestedFunction():
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        ## @var __privateAttr
        # @hideinitializer
        # @private
        __privateAttr = __privateFunctionAttr
        ## @var _protectedAttr
        # @hideinitializer
        # @protected
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction
