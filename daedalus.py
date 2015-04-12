#!/usr/bin/python
# Core file. Contains all classes, and methods to read and write back RSA
# public and private keys
# Also the only file to be executed
# Contributor: Sushant Dinesh [:sushant94]

import getopt
import struct
import sys
import gmpy

import pyasn1_modules.rfc3447
import pyasn1.codec.ber.encoder
from base64 import b64decode
from base64 import b64encode

# Local module imports
from weiner import Weiner

class RSAKey:
    def __init__(self):
        """ 
        A RSA Key is represented by:
          * N    = Modulus = p * q
          * p, q = Primes
          * e    = Public Exponent
          * d    = Private Exponent
          * phin = Euler Toitent of N
        """
        self.n = None
        self.p = None
        self.q = None
        self.e = None
        self.d = None
        self.phin = None
        self.outfile = None

    def ParsePublicKey(self, infile):
        f = open(infile, 'r')
        s = f.read()
        f.close()
        parts = []
        keydata = b64decode(s)
        while keydata:
            dlen = struct.unpack('>I', keydata[:4])[0]
            data, keydata = keydata[4:dlen+4], keydata[4+dlen:]
            parts.append(data)
        self.e = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[1]]))
        self.n = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[2]]))

    def MakePrivateKey(self):
        key = pyasn1_modules.rfc3447.RSAPrivateKey()
        dp = self.d % (self.p - 1)
        dq = self.d % (self.q - 1)
        qInv = gmpy.invert(self.q, self.p)

        key.setComponentByName('version', 0)
        key.setComponentByName('modulus', self.n)
        key.setComponentByName('publicExponent', self.e)
        key.setComponentByName('privateExponent', self.d)
        key.setComponentByName('prime1', self.p)
        key.setComponentByName('prime2', self.q)
        key.setComponentByName('exponent1', dp)
        key.setComponentByName('exponent2', dq)
        key.setComponentByName('coefficient', qInv)
        
        ber_key = pyasn1.codec.ber.encoder.encode(key)
        pem_key = b64encode(ber_key).decode("ascii")
        out = ['-----BEGIN RSA PRIVATE KEY-----']
        out += [pem_key[i:i + 64] for i in range(0, len(pem_key), 64)]
        out.append('-----END RSA PRIVATE KEY-----\n')
        out = "\n".join(out)
        if not self.outfile == None:
            f = open(self.outfile, 'w')
            f.write(out.encode('ascii'))
            f.close()
        else:
            print out.encode("ascii")


help_msg =\
"""
Welcome to Daedalus v0. Security is very Critical!
Options:
    -h          Display this help menu
    -i          Input a Public Key file
    -I          Input a Private Key file
    -a          Attack Name to try
    -o          Write results to file (defaults to stdout)
    -l          Lists all available attacks
"""

attacks_help =\
"""
Available Attacks:
------------------------
* Weiner's attack for small private key exponent (-a weiner)
"""

def attack(key, name):
    if name == "weiner":
        print "Trying Weiner Attack"
        w = Weiner(key)
        w.hack()
        key.MakePrivateKey()

def main(argv):
    key = RSAKey()
    try:
        opts, args = getopt.getopt(argv, "h:i:I:o:a:l:", [])
    except getopt.GetoptError:
        print help_msg
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print help_msg
        if opt == "-l":
            print attacks_help
        if opt == "-i":
            key.ParsePublicKey(arg)
        if opt == "-o":
            key.outfile = arg
        if opt == "-a":
            attack(key, arg)

if __name__ == "__main__":
    main(sys.argv[1:])
   
