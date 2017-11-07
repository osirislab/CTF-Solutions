def get_flag(start):
    s = ""
    r7 = 0
    r0 = start
    r8 = 0
    while r8 <= 20:
        if True:  # all of the checks are broken (47 < a < 58 means (47 < a) < 58)
            s += chr(r0)
        if r7 == 2:
            r0 ^= 4
        if r7 >= 1:
            r0 ^= 3
        r0 += 5
        if r0 > 122:
            r7 += 1
            s += '_'
            r0 = 66
        if r0 < 48:
            r0 += 30
        r8 += 1
    return s

print "ASIS{%s}" % get_flag(65)