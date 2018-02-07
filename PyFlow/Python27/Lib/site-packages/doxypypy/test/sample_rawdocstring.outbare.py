#!/usr/bin/env python
# encoding: utf-8
##
#Raw docstrings sample module.
#
#Tests support for raw docstrings, which are necessary when docstrings contain
#escape sequences.
#
#E.g. TeX-maths:
#@f[
#  \exp(x) = \sum_{k=0}^{\infty} \frac{x^k}{k!}
#@f]
#
#Related to issue #8 [1].
#
#[1]: https://github.com/Feneric/doxypypy/issues/8
#


##Calculate the square-root of four.
#
#    Returns:
#        @f$ \sqrt{4} @f$.
#
def sqrt4():
    return 2


##Invert the given number.
#
#    Args:
#        x:  Invert this number \f$x\f$.
#
#    Returns:
#        @f$\frac{1}{x}@f$.
#
def invert(x):
    return 1/x


##Stores a polynomial.
#
#    Here, a polynomial is defined as a finite series of the form
#    @f[
#      a_0 + a_1 x + a_2 x^2 + \cdots + a_N x^N,
#    @f]
#    where \f$ a_k \f$, for \f$k=0,\ldots,N\f$, are real coefficients, and
#    \f$N\f$ is the degree of the polynomial.
#
#    Attributes:
#        coefficients:  A list of coefficients.
#
class Polynomial(object):

    ##Initialize a polynomial instance.
    #
    #        Args:
    #            coefficients:  A list of coefficients. Beginning with \f$a_0\f$,
    #                           and ending with \f$a_N\f$.
    #
    def __init__(self, coefficients):
        self.coefficients = coefficients


    ##Find the real roots of the polynomial.
    #
    #        I.e. all real numbers @f$ x_i @f$ for which
    #        \f[
    #          a_0 + a_1 x_i + a_2 {x_i}^2 + \cdots + a_N {x_i}^N = 0.
    #        \f]
    #
    #        Returns:
    #            A list of all real roots, or an empty list if there are none.
    #
    #        \todo Implement this method.
    #
    def find_roots(self):
        pass


##Demonstrate polynomial class.
def main():
    p = Polynomial([0, 1, 0, 2])

    print(p.coefficients)


if __name__ == '__main__':
    main()
