#!/usr/bin/env python
# As close as possible to a direct copy of the sample in PEP 257 and still
# be valid code. Simple as can be.

complex_zero = 0j


def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)

    """
    if imag == 0.0 and real == 0.0:
        return complex_zero
    else:
        return complex(real, imag)
