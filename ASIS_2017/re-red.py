import requests

base = "https://re-red.asis-ctf.ir/"
url = "index.html"

for i in range(1000):
    r = requests.get(base+url).text
    url = r.split('0; url=')[1].split('">')[0]
    img = r.split('<img src="')[1].split('">')[0]
    print url,img
    if 'ASIS' in r:
        print r
    if img != './images/skate-{}.jpg'.format(i % 4):
        print "WEIRD"