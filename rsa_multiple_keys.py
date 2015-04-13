# Attacks when we multiple RSA Public keys available
#   * Attack 1: Same e. Different N. (N_i, N_j) != 1 for some i, j
#   * Attack 2:

import sys
import daedmath

class MultiKey:
    def __init__(self, keys):
        if not keys:
            print "ERROR: No Keys Loaded"
            sys.exit(2)
        self.keys = keys

    def hack(self):
        # First Attack: Check if any two keys have (N_i, N_j) != 1
        for i in range(len(self.keys)):
            for j in range(i + 1, len(self.keys)):
                gcd = daedmath.euclid(self.keys[i].n, self.keys[j].n)
                if gcd != 1:
                    self.keys[i].p = gcd
                    self.keys[i].q = self.keys[i].n / gcd
                    self.keys[i].phin = self.keys[i].n + 1 - self.keys[i].p - self.keys[i].q
                    self.keys[i].d = self.keys[i].phin / self.keys[i].e
                    print self.keys[i].p
                    print self.keys[i].q
                    self.keys[i].MakePrivateKey()
                    self.keys[j].p = gcd
                    self.keys[j].q = self.keys[j].n / gcd
                    self.keys[j].phin = self.keys[j].n + 1 - self.keys[j].p - self.keys[j].q
                    self.keys[j].d = self.keys[j].phin / self.keys[j].e
                    print self.keys[j].p
                    print self.keys[j].q
                    self.keys[j].MakePrivateKey()
