# Contributor: Sushant Dinesh [:sushant94]

import gmpy
import daedmath
import math
import sys
import sympy
from fractions import Fraction

class Weiner:
    """
    Weiner Attack for low private key exponent.
    More Information: http://en.wikipedia.org/wiki/Wiener%27s_attack
    """
    def __init__(self, key):
        self.key = key
        # Perform checks to see if the key is filled in with required data
        if self.key.e == None or self.key.n == None:
            print "ERROR: Public Key not loaded\n"
            sys.exit(2)

    # Check if the guessed k/d is correct
    def verify(self, f):
        k = f.numerator
        d = f.denominator
        phin = (self.key.e * d - 1) / k
        B = self.key.n - phin + 1
        det = (B * B) - (4 * 1 * self.key.n) 
        if det > 0 and gmpy.is_square(det):
            self.key.d = d
            self.key.phin = phin
            return True
        else:
            return False

    def getFrac(self, l, i):
        f = Fraction()
        while i >= 0:
            f = Fraction(1, l[i] + f)
            i -= 1
        return Fraction(1, f)

    def computePQ(self):
        p_val = sympy.Symbol('p_val')
        eq = sympy.Eq(p_val * p_val + (self.key.n + 1 - self.key.phin) * p_val + self.key.n)
        solved = sympy.solve(eq, p_val)
        self.key.p = int(-1*(solved[0]))
        self.key.q = int(-1*(solved[1]))

    # All modules developed must have this method hack() which calls other methods to break RSA!
    def hack(self):
        l = daedmath.computeContinuedFractions(self.key.e, self.key.n)
        for i in range(len(l)):
            if l[i] == 0:
                continue
            f = self.getFrac(l, i)
            if self.verify(f):
                self.computePQ()
                break
