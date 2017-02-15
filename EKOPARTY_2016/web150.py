import requests, random

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(card_number[count])

        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    return ( (sum % 10) == 0 )

def luhn(l, r, filler_n):
    filler = ''.join(str(x) for x in random.sample(range(0,10), filler_n))
    for i in range(0, 10):
        if cardLuhnChecksumIsValid(l+filler+str(i)+r):
            return filler+str(i)

HEADERS = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'en-US,en;q=0.8',
           'Content-Type': 'application/json',
           'Cookie': 'ekocard3r=slnqEBpaKFftyKByvBDrDn0q0o1',
           'Origin': 'http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000',
           'Referer': 'http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000/',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           }

nums = requests.post('http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000/api.php',
                     data='{"action":"start"}', headers=HEADERS).json()

print nums

cards = {'visa': 4, 'mcard': 7, 'amex': 6}

resp = {}

for card, n_filler in cards.iteritems():
    p = nums['p'+card]
    s = nums['s'+card]
    
    resp['n'+card] = luhn(p, s, n_filler)
    print card, p+resp['n'+card]+s

print resp

print requests.post('http://86dc35f7013f13cdb5a4e845a3d74937f2700c7b.ctf.site:20000/api.php',
                    data='{"nvisa":"'+resp['nvisa']+'","nmcard":"'+resp['nmcard']+'","namex":"'+resp['namex']+'","action":"validate"}',
                    headers=HEADERS).json()