# py file to hold general math functions
# Contributors: Sushant Dinesh [:sushant94]
#

# Returns an array of upto 10^5 Continued fraction coeffs
def computeContinuedFractions(a, b):
    cFracs = []
    for i in range(10000):
        n = a / b
        r = a - (b * n)
        a, b = b, r
        cFracs.append(n)
        if r == 0:
            break
    return cFracs

def euclid(a, b):
    gcd = 1
    while b != 0:
        n = a // b
        r = a - (b * n)
        if r == 0:
            break
        a, b = b, r
        gcd = r
    return gcd

# returns (gcd, X, Y) . gcd(a, b) = aX + bY
def extendedEuclid(a, b):
    gcd = 1
    s = 0
    s_ = 1
    t = 1
    t_ = 0
    while b != 0:
        n = a // b
        r = a - (b * n)
        if r == 0:
            break
        a, b = b, r
        gcd = r
        s, s_ = s_ - n * s, s
        t, t_ = t_ - n * t, t
    return gcd, s, t

def invert(a, b):
    gcd, x, y = extendedEuclid(a, b)
    return x

# Linear Congruence is of the form: ax = b mod c
def solveLinearCongruence(a, b, c):
    gcd, x, y = extendedEuclid(a, c)
    y = -1 * y
    x = x * b
    solns = []
    end = c
    if c > 10000:
        end = 10000
    for k in range(0,end):
        s = (x + (c * k)) % c
        solns.append(s)
    return list(set(solns))


# Test Functions to verify working
def TcomputeContinuedFractions():
    l = computeContinuedFractions(17993, 90581)
    expected = [0, 5, 29, 4, 1, 3, 2, 4, 3]
    if l == expected:
        print "Test Compute Continued Fractions: Passed!"
    else:
        print "Test Compute Continued Fractions: Failed!"

def Teuclid():
    expected = 17
    if expected == euclid(42823, 6409):
        print "Test Euclid: Passed!"
    else:
        print "Test Euclid: Failed!"

def TextendedEuclid():
    expected = (17, -22, 147)
    if expected == extendedEuclid(42823, 6409):
        print "Test ExtendedEuclid: Passed!"
    else:
        print "Test ExtendedEuclid: Failed!"


def TsolveLinearCongruence():
    solns = solveLinearCongruence(9, 15, 23)
    expected = [17]
    if expected == solns:
        print "Test solveLinearCongruence: Passed!"
    else:
        print "Test solveLinearCongruence: Failed!"


if __name__ == "__main__":
    TcomputeContinuedFractions()
    Teuclid()
    TextendedEuclid()
    TsolveLinearCongruence()
