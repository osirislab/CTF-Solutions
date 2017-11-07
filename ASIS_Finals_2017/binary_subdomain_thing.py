import dns.resolver

x=dns.resolver.Resolver()
x.nameservers=['95.85.26.168']

orig='01100101011111010110111101100101010010010110010101000001.asisctf.com'

while True:
    try:
        x.query('0'+orig)
        append = '0'
    except KeyboardInterrupt:
        break
    except dns.resolver.NoNameservers:
        append = '1'
    orig = append+orig
    if orig.index('.') == 63:
        orig = '.'+orig
    print(orig)