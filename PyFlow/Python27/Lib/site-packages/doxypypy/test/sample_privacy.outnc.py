# -*- coding: utf-8 -*-
## @brief Typical class with private members.
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


## @brief     A sample new-style class.
#
#    Nothing special, just a basic new-style class that has some
#    private and protected members in it.
#
# @namespace sample_privacy.NewStyleSample

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

    ## @brief         This constructor won't be private.
    #
    # @namespace sample_privacy.NewStyleSample.__init__

    def __init__(self):
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    ## @brief         This will be not be private.
    #
    # @namespace sample_privacy.NewStyleSample.__notPrivateClassMethod__

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

    ## @brief         This will be private.
    #
    # @namespace sample_privacy.NewStyleSample.__privateClassMethod
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

    ## @brief         This will be protected.
    #
    # @namespace sample_privacy.NewStyleSample._protectedClassMethod
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

    ## @brief         This will be public.
    #
    # @namespace sample_privacy.NewStyleSample.publicClassMethod

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

    ## @brief         This static method will be public.
    #
    # @namespace sample_privacy.NewStyleSample.publicClassStaticMethod

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

    ## @brief         This class method will be public.
    #
    # @namespace sample_privacy.NewStyleSample.publicClassClassMethod

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

    ## @brief         An inner not private class.
    #
    #        Nothing special, just a not private helper class.
    #
    # @namespace sample_privacy.NewStyleSample.__innerNotPrivate__

    class __innerNotPrivate__(object):
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.NewStyleSample.__innerNotPrivate__.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ## @brief         An inner protected class.
    #
    #        Nothing special, just a protected helper class.
    #
    # @namespace sample_privacy.NewStyleSample.__innerProtected
    # @private

    class __innerProtected(object):
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.NewStyleSample.__innerProtected.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ## @brief         An inner private class.
    #
    #        Nothing special, just a private helper class.
    #
    # @namespace sample_privacy.NewStyleSample.__innerPrivate
    # @private

    class __innerPrivate(object):
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.NewStyleSample.__innerPrivate.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


## @brief     A sample old-style class.
#
#    Nothing special, just a basic old-style class that has some
#    private and protected members in it.
#
# @namespace sample_privacy.OldStyleSample

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

    ## @brief         This constructor won't be private.
    #
    # @namespace sample_privacy.OldStyleSample.__init__

    def __init__(self):
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    ## @brief         This will be not be private.
    #
    # @namespace sample_privacy.OldStyleSample.__notPrivateClassMethod__

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

    ## @brief         This will be private.
    #
    # @namespace sample_privacy.OldStyleSample.__privateClassMethod
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

    ## @brief         This will be protected.
    #
    # @namespace sample_privacy.OldStyleSample._protectedClassMethod
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

    ## @brief         This will be public.
    #
    # @namespace sample_privacy.OldStyleSample.publicClassMethod

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

    ## @brief         This static method will be public.
    #
    # @namespace sample_privacy.OldStyleSample.publicClassStaticMethod

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

    ## @brief         This class method will be public.
    #
    # @namespace sample_privacy.OldStyleSample.publicClassClassMethod

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

    ## @brief         An inner not private class.
    #
    #        Nothing special, just a not private helper class.
    #
    # @namespace sample_privacy.OldStyleSample.__innerNotPrivate__

    class __innerNotPrivate__():
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.OldStyleSample.__innerNotPrivate__.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ## @brief         An inner protected class.
    #
    #        Nothing special, just a protected helper class.
    #
    # @namespace sample_privacy.OldStyleSample.__innerProtected
    # @private

    class __innerProtected():
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.OldStyleSample.__innerProtected.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    ## @brief         An inner private class.
    #
    #        Nothing special, just a private helper class.
    #
    # @namespace sample_privacy.OldStyleSample.__innerPrivate
    # @private

    class __innerPrivate():
        ## @brief             This constructor won't be private.
        #
        # @namespace sample_privacy.OldStyleSample.__innerPrivate.__init__

        def __init__(self):
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


## @brief     A sample function.
#
#    Nothing special, just a basic function that has some private
#    and protected variables in it.
#
# @namespace sample_privacy.Function

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

    ## @brief         This will not be private.
    #
    # @namespace sample_privacy.Function.__notPrivateFunction__

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

    ## @brief         This will be private.
    #
    # @namespace sample_privacy.Function.__privateNestedFunction
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

    ## @brief         This will be protected.
    #
    # @namespace sample_privacy.Function._protectedNestedFunction
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

    ## @brief         This will be public.
    #
    # @namespace sample_privacy.Function.publicNestedFunction

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


## @brief     A sample protected function.
#
#    Nothing special, just a basic protected function that has some
#    private and protected variables in it.
#
# @namespace sample_privacy._ProtectedFunction
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

    ## @brief         This will not be private.
    #
    # @namespace sample_privacy._ProtectedFunction.__notPrivateFunction__

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

    ## @brief         This will be private.
    #
    # @namespace sample_privacy._ProtectedFunction.__privateNestedFunction
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

    ## @brief         This will be protected.
    #
    # @namespace sample_privacy._ProtectedFunction._protectedNestedFunction
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

    ## @brief         This will be public.
    #
    # @namespace sample_privacy._ProtectedFunction.publicNestedFunction

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


## @brief     A sample private function.
#
#    Nothing special, just a basic private function that has some
#    private and protected variables in it.
#
# @namespace sample_privacy.__PrivateFunction
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

    ## @brief         This will not be private.
    #
    # @namespace sample_privacy.__PrivateFunction.__notPrivateFunction__

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

    ## @brief         This will be private.
    #
    # @namespace sample_privacy.__PrivateFunction.__privateNestedFunction
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

    ## @brief         This will be protected.
    #
    # @namespace sample_privacy.__PrivateFunction._protectedNestedFunction
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

    ## @brief         This will be public.
    #
    # @namespace sample_privacy.__PrivateFunction.publicNestedFunction

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
