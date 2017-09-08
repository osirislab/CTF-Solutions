enc = '7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e'.decode('hex')
orig = 'TWCTF{'
key = ''

for i in range(len(orig)):
    key += chr((ord(enc[i+1]) - ord(orig[i]) - ord(enc[i])) % 128)

print(key)

start_of_plaintext_key = len(enc) - 13

l = len(key)
for i in range(start_of_plaintext_key + l, len(enc)): # i is the index into enc
    key += chr((ord(enc[i]) - ord(key[(i-1) % 13]) - ord(enc[i-1])) % 128)

print(key)

dec = ''
for i in range(1, len(enc)):
    dec += chr((ord(enc[i]) - ord(key[(i-1) % 13]) - ord(enc[i-1])) % 128)
print(dec)