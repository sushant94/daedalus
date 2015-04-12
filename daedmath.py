# py file to hold general math functions
# Contributors: Sushant Dinesh [:sushant94]
#

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

# Test Functions to verify working
def TcomputeContinuedFractions():
    l = computeContinuedFractions(17993, 90581)
    expected = [0, 5, 29, 4, 1, 3, 2, 4, 3]
    if l == expected:
        print "passed!"
    else:
        print "failed!"

