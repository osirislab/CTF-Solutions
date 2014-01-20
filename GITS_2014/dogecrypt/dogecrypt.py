from zipfile import _ZipDecrypter
import string
import itertools
import tqdm
import sys

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, maxlength + 1)))

def percentage_printable(text):
    x = 0.0
    for c in text:
        if c in string.printable:
            x += 1
    return x / len(text)

fp = open(sys.argv[1], 'rb')
print sys.argv[1]
text = fp.read(12)
words = open('american-english-small', 'r')


# for attempt in tqdm.tqdm(bruteforce(string.ascii_letters + string.digits, 10)):
for attempt in tqdm.tqdm(words):
    zd = _ZipDecrypter(attempt.rstrip())
    fp.seek(12)
    res = ''.join(zd(c) for c in fp.read())

    try:
        p = percentage_printable(res)
    except:
        p = 0 
    if p > 0.95:
        print p, repr(res), attempt
        exit()

fp.close()
