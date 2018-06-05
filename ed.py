#
# The below is a __doc__ comment
#
"Explaining decimal versus binary floating point"
import tiny

class MyImporter(object):
    "trivial meta_path hook"
    
    def find_module(self, fullname, path=None):
        "prevent loading of the C implementation of decimal"
        
        if 0:
            print("find_module({},{})".format(fullname,path))
        if fullname == "_decimal":
            raise ImportError
        else:
            return None

import sys
sys.meta_path.insert(0,MyImporter())

import decimal
from decimal import Decimal
import fractions
from fractions import Fraction

sys.meta_path.pop(0)

class MyDecimal(Decimal):
    "Bignum class for decimal arithmetic."
    
    def __str__(self, eng=False, context=None):
        """Return string representation of the number in scientific notation.

        The only differnce from the original is "True or" so it will
        avoid using scientific/engineering notation"""

        sign = ['', '-'][self._sign]
        if self._is_special:
            if self._exp == 'F':
                return sign + 'Infinity'
            elif self._exp == 'n':
                return sign + 'NaN' + self._int
            else: # self._exp == 'N'
                return sign + 'sNaN' + self._int

        # number of digits of self._int to left of decimal point
        leftdigits = self._exp + len(self._int)

        # dotplace is number of digits of self._int to the left of the
        # decimal point in the mantissa of the output string (that is,
        # after adjusting the exponent)
        if True or self._exp <= 0 and leftdigits > -6:
            # no exponent required
            dotplace = leftdigits
        elif not eng:
            # usual scientific notation: 1 digit on left of the point
            dotplace = 1
        elif self._int == '0':
            # engineering notation, zero
            dotplace = (leftdigits + 1) % 3 - 1
        else:
            # engineering notation, nonzero
            dotplace = (leftdigits - 1) % 3 + 1

        if dotplace <= 0:
            intpart = '0'
            fracpart = '.' + '0'*(-dotplace) + self._int
        elif dotplace >= len(self._int):
            intpart = self._int+'0'*(dotplace-len(self._int))
            fracpart = ''
        else:
            intpart = self._int[:dotplace]
            fracpart = '.' + self._int[dotplace:]
        if leftdigits == dotplace:
            exp = ''
        else:
            if context is None:
                context = getcontext()
            exp = ['e', 'E'][context.capitals] + "%+d" % (leftdigits-dotplace)

        return sign + intpart + fracpart + exp

"""
Rough equivalent of:
BC_LINE_LENGTH=$COLUMNS bc << //
scale=123
for (i=0;i<=123;++i)
   print i,"\t",2^i+2^-i,"\n"
//
"""
decimal.getcontext().prec *= 1

D0 = Decimal(0)
D1 = Decimal(1)
D2 = Decimal(2)

def f(arg):
    return D0+D1*D2**(+i)+D1*D2**(-i)

if __name__ == '__main__':
    try:
        n = int(sys.argv[1])
    except:
        n = 123
else:
    n = 0

for i in range(n):
    x = Decimal(f(i))
    print(x)
for i in range(n):
    x = MyDecimal(f(i))
    print(x)
for i in range(n):
    x = Fraction.from_decimal(f(i))
    print(x)

if range(n):
    del i,x
del D0,D1,D2,f,n
# EOF
