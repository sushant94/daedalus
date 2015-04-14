# ElGamal Cryptanalysis Module.
# Contributor: Sushant Dinesh [:sushant94]

# Read Multiple signatures (r, s, m) from a JSON file.
# Check if the private factor is vulnerable due to re-use of 'r'

'''
JSON Input Format:
====================
{ 
   "generator": ... , "safeprime": ... , "pubkey": ... ,
   "sigs": [
              {"s": ... , "r": ... , "m": ... },
                          ... 
           ]
}
'''

import json
import sys
import hashlib
import gmpy

import daedmath

class Elgamal:
    def __init__(self, infile):
        f = open(infile, 'r')
        json_data = f.read()
        json_data.strip
        data = json.loads(json_data, encoding="utf8")
        self.generator = data["generator"]
        self.safeprime = data["safeprime"]
        self.pubkey = data["pubkey"]
        self.sigs = data["sigs"]
        if (not self.generator or not self.safeprime
             or not self.pubkey or not self.sigs):
                print "ERROR: Unable to load file. Please check JSON format"
                sys.exit(2)

    def verify(self, i):
        sig = self.sigs[i]
        if sig["r"] <= 0 or sig["r"] >= self.safeprime:
            return False
        if sig["s"] <= 0 or sig["s"] >= self.safeprime - 1:
            return False
        h = int(hashlib.sha384(sig["m"].encode("utf8")).hexdigest(), 16)
        left = pow(self.generator, h, self.safeprime)
        right = (pow(self.pubkey, sig["r"], self.safeprime) * pow(sig["r"], sig["s"], self.safeprime)) % self.safeprime
        return left == right

    def hack(self):
        print "[*] Initialized Elgamal ..."
        t = 0
        t_ = 0
        flag = 0
        # First select two sigs which are valid and have the same r
        for i in range(len(self.sigs)):
            t = self.sigs[i]
            for j in range(i + 1, len(self.sigs)):
                t_ = self.sigs[j]
                if t["r"] != t_["r"]:
                    continue
                if not self.verify(j) or not self.verify(i):
                    continue
                flag = 1
                break
            if flag == 1:
                break

        if flag == 0:
            print "[X] Signatures are secure"
            sys.exit(2)
        
        print "[*] Found sigs with common r! Trying to break."

        s1 = t["s"]
        s2 = t_["s"]
        m1 = int(hashlib.sha384(t["m"]).hexdigest(), 16)
        m2 = int(hashlib.sha384(t_["m"]).hexdigest(), 16)
        m1_m2 = m1 - m2

        n = daedmath.euclid(s1 - s2, self.safeprime -1)
        k_ = gmpy.divm(m1_m2 / n, (s1 - s2) / n, (self.safeprime-1)/n)
        k = None
        for i in range(0, n):
            k = k_ + (i * (self.safeprime - 1) / n)
            if pow(self.generator, k, self.safeprime) == t["r"]:
                break
        if not k:
            print "[X] Failed to get a valid k!"
            sys.exit(2)
        
        print "[*] Found k: %d" % k
        n = daedmath.euclid(t["r"], self.safeprime - 1)
        side2 = m1 - k * t["s"]
        x_ = gmpy.divm(side2/n, t["r"]/n, (self.safeprime - 1) / n)
        x = None
        for i in range(0, n):
            x = x_ + (i * (self.safeprime - 1) / n)
            if pow(self.generator, x, self.safeprime) == self.pubkey:
                break
        if x:
            print "[*] Retrieved Private Key x: %d" % x
        
e = Elgamal("tests/dist/sigs.txt")
e.hack()
