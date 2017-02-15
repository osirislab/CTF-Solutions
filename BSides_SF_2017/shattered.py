from pcapfile import savefile
f=open('/Users/nickgregory/Downloads/shattered.pcap','rb')
cap=savefile.load_savefile(f)

match = "\xff\xd8\xff\xe0\x00\x10JFIF"
assembled = match
best = None
used = []

while True:
    for i, pkt in enumerate(cap.packets):
        data = pkt.raw()[54:]
        if match in data:
            offset = data.index(match)
            if len(data) - offset > best and i not in used:
                best = i
    
    if best is None:
        break
    data = cap.packets[best].raw()[54:]
    offset = data.index(match)
    print "Best match of ", match.encode('hex'), "is at pkt idx", best, "offset", offset
    
    assembled += data[offset+len(match):]
    match = data[-10:]
    used.append(best)
    best = None

f = open('out.jpg', 'wb')
f.write(assembled)
f.close()