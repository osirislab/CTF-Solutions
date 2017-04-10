import sys

# 1. Get the input file by neutering "unlink" with:
#       int unlink(const char *pathname) {
#           return 0;
#       }
# compile with `gcc -shared -fpic -o neuter.so neuter.c
# 2. grab flag.enc from the generated tempdir (It's included here as "cobra_flag.enc")
# 3. Decrypt flag with this script (they just flip all the nibbles, so will we)
# 4. ez points

with open(sys.argv[1], 'r') as f:
    cz = bytearray(f.read())

for i, x in enumerate(cz):
    a, b = ((x & 0xF0) >> 4), ((x & 0x0F) << 4)
    cz[i] = a | b

with open(sys.argv[2], 'w') as f:
    f.write(cz)
