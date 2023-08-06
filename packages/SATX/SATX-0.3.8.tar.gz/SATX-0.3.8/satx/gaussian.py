"""
Copyright (c) 2012-2021 Oscar Riveros [https://twitter.com/maxtuno].

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from .unit import *


class Gaussian:
    def __init__(self, x, y):
        self.real = x
        self.imag = y

    def __eq__(self, other):
        assert self.real == other.real
        assert self.imag == other.imag
        return True

    def __ne__(self, other):
        bit = Unit(self.real.alu, bits=2)
        assert (self.real - other.real).iff(bit[0], self.imag - other.imag) != 0
        return True

    def __neg__(self):
        return Gaussian(-self.real, -self.imag)

    def __add__(self, other):
        return Gaussian(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Gaussian(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Gaussian((self.real * other.real) - (self.imag * other.imag), ((self.real * other.imag) + (self.imag * other.real)))

    def __truediv__(self, other):
        return Gaussian(
            ((self.real * other.real) + (self.imag * other.imag)) / (other.real ** 2 + other.imag ** 2), ((self.imag * other.real) - (self.real * other.imag)) / (other.real ** 2 + other.imag ** 2))

    def __pow__(self, power, modulo=None):
        other = self
        for _ in range(power - 1):
            other *= self
        return other

    def __abs__(self):
        return Gaussian(self.real.alu.sqrt(self.real ** 2 + self.imag ** 2), 0)

    def __repr__(self):
        return '({}+{}j)'.format(self.real, self.imag)

    def __str__(self):
        return str(self.__repr__())

    def __complex__(self):
        return complex(int(self.real), int(self.imag))

    def conjugate(self):
        return Gaussian(self.real, -self.imag)
