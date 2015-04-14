# sage file to recover entire private key from a few bits of leak
# p_ is the leaked bits of the prime p.
# It can be considered an approximation of the original complete p
# Coppersmith: N = pq. we have an approximation p_ of p with |p - p_| <= N^1/4 then we can factorize N in polynomial in log(n)
def hack(p_, N):
    F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
    f = x - p_
    p_ = p_ - f.small_roots(X=2^180, beta = 0.4)[0]
    q = N / int(p_)
    print "p: %s\nq: %s" % (hex(int(p_)), hex(int(q)))
    print int(N) == int(p_) * q

p = 0x00F114805F133F011E29D59D931FAD8AAF8069CE3C2A8A5DE9A3F947DE0A511291ED170C4B5B09B020D70000000000000000000000000000000000000000000000
N = 0x00EED3C56E80324AFC7AB136015B7D35E573B0694D883D06F2BD1C9A85059A01AED598E0721820F0B0EAFF099C4EA5D2F59263E9B75C7782001000D5E967C35D1C29AFF6E2AC7C5A5D1BB5B49C404993C2C49EB8B10F3B6EE549B0E930E41A5A27FDF2BB8F0B60139C2A95B64737461E65FE551AFA66200C459A29D8EF45116791
hack(p, N)
