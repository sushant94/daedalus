#!/usr/bin/python
# Core file. Contains all classes, and methods to read and write back RSA
# public and private keys
# Also the only file to be executed
# Contributor: Sushant Dinesh [:sushant94]

import getopt
import struct
import sys
import gmpy
import os
from Crypto.PublicKey import RSA

import pyasn1_modules.rfc3447
import pyasn1.codec.ber.encoder
from base64 import b64decode
from base64 import b64encode

# Local module imports
from weiner import Weiner
from rsa_multiple_keys import MultiKey

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

def parsePEM(arg):
    f = open(arg, 'r')
    key64 = f.read()
    key64.strip
    keyDER = b64decode(key64)
    keyPub = RSA.importKey(keyDER)
    key = RSAKey()
    key.n = keyPub.n
    key.e = keyPub.e
    return key

def multiIn(arg):
    if not os.path.isdir(arg):
        return None
    l = os.listdir(arg)
    keys = []
    for i in range(len(l)):
        keys.append(parsePEM(arg+"/"+l[i]))
    return keys

help_msg =\
"""
Welcome to Daedalus v0. Security is very Critical!
Options:
    -h          Display this help menu
    -i          Input a Public Key file
    -mi         Multi-In. Used to load a folder of public keys
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
* Partial Key Exposure                           (-a partial)
* Multiple RSA Public Keys                       (-a multipub)
"""

def attack(key, keys, name):
    if name == "weiner":
        print "Trying Weiner Attack"
        w = Weiner(key)
        w.hack()
        key.MakePrivateKey()
    if name == "multipub":
        print "Trying To Break Using Multiple Public Keys"
        a = MultiKey(keys)
        a.hack()

def main(argv):
    key = RSAKey()
    keys = []
    try:
        opts, args = getopt.getopt(argv, "h:i:I:m:o:a:l:", [])
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
        if opt == "-m":
            # Returns an array of parsed keys.
            keys = multiIn(arg)
            key = None
        if opt == "-o":
            key.outfile = arg
        if opt == "-a":
            attack(key, keys, arg)

if __name__ == "__main__":
    main(sys.argv[1:])
   
