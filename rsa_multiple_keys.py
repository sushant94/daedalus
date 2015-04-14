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
        print "[*] Factoring of 2 keys using GCD"
        flag = False
        for i in range(len(self.keys)):
            for j in range(i + 1, len(self.keys)):
                gcd = daedmath.euclid(self.keys[i].n, self.keys[j].n)
                if gcd != 1:
                    flag = True
                    print " [*] Success"
                    for k in [i, j]:
                        self.keys[k].p = gcd
                        self.keys[k].q = self.keys[k].n / gcd
                        self.keys[k].phin = self.keys[k].n + 1 - self.keys[k].p - self.keys[k].q
                        self.keys[k].d = self.keys[k].phin / self.keys[k].e
                        self.keys[k].MakePrivateKey()
        if not flag:
            print "[X] Failed"
