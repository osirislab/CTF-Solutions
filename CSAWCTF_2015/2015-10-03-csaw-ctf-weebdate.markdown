---
author: ghost
comments: true
date: 2015-10-03 11:37+00:00
layout: post
slug: csaw-ctf-weebdate
title: CSAW CTF 2015 - Weebdate
---

After creating an account on the site and logging in, we notice pretty quickly that trying to set our profile image URL to an invalid URL returns a python error

```python
Malformed url ParseResult(scheme='', netloc='', path=u'asdf', params='', query='', fragment='')
```

If we set the URL to a valid URL (but not an image), the source of the page is returned. We tried a number of things to try and use this to get an arbitrary file read, but eventually gave up for the time being and went on looking for more bugs.

After looking at the raw responses, we noticed that a CSP was in place with a valid URL for reporting CSP violations. Seeing that this website was for a CTF, we assumed that there was some vulnerability in the CSP reporting/viewing, as it would otherwise be pointless (and far too much trouble to be a red herring). After finding the URL to view CSP violations, we found that the id part of the URL was vulnerable to plain and simple SQLi: `/csp/view/{SQL injection}`. We used sqlmap to dump the database, which gave us all the data we could need to generate the TOTP key. However we were still missing the exact algorithm (and the password).

After going back to the profile image URL issue discovered earlier, we discovered that we can abuse the issue to get a local file read by using the URI scheme `file://localhost/path/to/file`. Attempting to read `/proc/self/*` doesn’t yield any immediate results since this python script was running under apache, so we tried guessing the python server file's path and eventually found that `/var/www/weebdate/server.py` was the main server. The server also referenced `utils.py` which we also grabbed. In these two files we found that the algorithm for TOTP key generation which was insecure:

utils.py

```python
def generate_seed(username, ip_address):
    return int(struct.unpack("I", socket.inet_aton(ip_address))[0]) + struct.unpack("I", username[:4].ljust(4,"0"))[0]

def get_totp_key(seed):
    random.seed(seed)
    return pyotp.random_base32(16, random)
```

server.py

```python
@app.route('/register', methods=['GET', 'POST'])
def show_registration():
    ...
    if request.method.lower() == "post":
        username = request.form.get('username') or ''
        password = request.form.get('password') or ''
        ...
        seed = utils.generate_seed(username, request.remote_addr)
        totp_key = utils.get_totp_key(seed)
        utils.register_user(username, password, request.remote_addr)
        ...
```

We used this along with our DB dump to generate donaldtrump’s TOTP key.

We noticed that the stored password was the sha256 of the username+password, which seemed secure. We also found that all references to the user’s password were be properly hashed and never leaked, which surprised us as that meant the only way to obtain the raw password was via bruteforce. After confirming this with CTF organizers, we setup hashcat to do an up to 5 character sha256 bruteforce with the format as `donaldtrump?a?a?a?a?a` After a few minutes, the password was revealed to be 'zebra'. `md5(TOTP+'zebra')` is the flag for the challenge.
