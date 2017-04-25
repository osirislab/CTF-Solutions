import zlib
f = open('zipper.zip').read()
for i in range(len(f)):
    try:
        print zlib.decompress(f[i:], -zlib.MAX_WBITS)
    except Exception as e:
        continue