# -*- coding: utf-8 -*-
"""
Typical class with private members.

Here we're just trying to make a fairly straightforward class
that has some private (Python-enforced private, name-mangled)
and protected (by convention only, a.k.a. "bed lump")
variables.
"""
__notPrivateModuleAttr__ = 1
__privateModuleAttr = 2
_protectedModuleAttr = 3


class NewStyleSample(object):
    """
    A sample new-style class.

    Nothing special, just a basic new-style class that has some
    private and protected members in it.
    """
    __notPrivateClassAttr__ = 1
    __privateClassAttr = 2
    _protectedClassAttr = 3

    def __init__(self):
        """
        This constructor won't be private.
        """
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    def __notPrivateClassMethod__(self):
        """
        This will be not be private.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def __privateClassMethod(self):
        """
        This will be private.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def _protectedClassMethod(self):
        """
        This will be protected.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def publicClassMethod(self):
        """
        This will be public.
        """
        public = 0
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.public = public
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    @staticmethod
    def publicClassStaticMethod():
        """
        This static method will be public.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    @classmethod
    def publicClassClassMethod(self):
        """
        This class method will be public.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    class __innerNotPrivate__(object):
        """
        An inner not private class.

        Nothing special, just a not private helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    class __innerProtected(object):
        """
        An inner protected class.

        Nothing special, just a protected helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    class __innerPrivate(object):
        """
        An inner private class.

        Nothing special, just a private helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


class OldStyleSample():
    """
    A sample old-style class.

    Nothing special, just a basic old-style class that has some
    private and protected members in it.
    """
    __notPrivateClassAttr__ = 1
    __privateClassAttr = 2
    _protectedClassAttr = 3

    def __init__(self):
        """
        This constructor won't be private.
        """
        self.__notPrivateAttr__ = 1
        self.__privateAttr = 2
        self._protectedAttr = 3

    def __notPrivateClassMethod__(self):
        """
        This will be not be private.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def __privateClassMethod(self):
        """
        This will be private.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def _protectedClassMethod(self):
        """
        This will be protected.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    def publicClassMethod(self):
        """
        This will be public.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr

    @staticmethod
    def publicClassStaticMethod():
        """
        This static method will be public.
        """
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    @classmethod
    def publicClassClassMethod(self):
        """
        This class method will be public.
        """
        public = 0
        __notPrivateAttr__ = 1
        __privateAttr = 2
        _protectedAttr = 3
        self.public = public
        self.__notPrivateAttr__ = __notPrivateAttr__
        self.__privateAttr = __privateAttr
        self._protectedAttr = _protectedAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    class __innerNotPrivate__():
        """
        An inner not private class.

        Nothing special, just a not private helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    class __innerProtected():
        """
        An inner protected class.

        Nothing special, just a protected helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3

    class __innerPrivate():
        """
        An inner private class.

        Nothing special, just a private helper class.
        """
        def __init__(self):
            """
            This constructor won't be private.
            """
            self.public = 0
            self.__notPrivateAttr__ = 1
            self.__privateAttr = 2
            self._protectedAttr = 3


def Function():
    """
    A sample function.

    Nothing special, just a basic function that has some private
    and protected variables in it.
    """
    __notPrivateFunctionAttr__ = 1
    __privateFunctionAttr = 2
    _protectedFunctionAttr = 3

    def __notPrivateFunction__():
        """
        This will not be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def __privateNestedFunction():
        """
        This will be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def _protectedNestedFunction():
        """
        This will be protected.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def publicNestedFunction():
        """
        This will be public.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction


def _ProtectedFunction():
    """
    A sample protected function.

    Nothing special, just a basic protected function that has some
    private and protected variables in it.
    """
    __notPrivateFunctionAttr__ = 1
    __privateFunctionAttr = 2
    _protectedFunctionAttr = 3

    def __notPrivateFunction__():
        """
        This will not be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def __privateNestedFunction():
        """
        This will be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def _protectedNestedFunction():
        """
        This will be protected.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def publicNestedFunction():
        """
        This will be public.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction


def __PrivateFunction():
    """
    A sample private function.

    Nothing special, just a basic private function that has some
    private and protected variables in it.
    """
    __notPrivateFunctionAttr__ = 1
    __privateFunctionAttr = 2
    _protectedFunctionAttr = 3

    def __notPrivateFunction__():
        """
        This will not be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def __privateNestedFunction():
        """
        This will be private.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def _protectedNestedFunction():
        """
        This will be protected.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    def publicNestedFunction():
        """
        This will be public.
        """
        __notPrivateAttr__ = __notPrivateFunctionAttr__
        __privateAttr = __privateFunctionAttr
        _protectedAttr = _protectedFunctionAttr
        return __notPrivateAttr__ + __privateAttr + _protectedAttr

    return __notPrivateFunction__ + __privateNestedFunction \
        + _protectedNestedFunction + publicNestedFunction
