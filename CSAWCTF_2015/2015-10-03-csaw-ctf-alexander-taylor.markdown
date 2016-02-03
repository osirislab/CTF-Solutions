---
author: qu4ckles
comments: true
date: 2015-09-21 11:37+00:00
layout: post
slug: csaw-ctf-alexander-taylor
title: CSAW CTF 2015 - Alexander Taylor
---

The first part of the challenge is to find the initals of the club Alex was in university. Googling "Alexander Taylor Raytheon" brings up his LinkedIn, which shows that he went to the University of South Florida and was president of the Whitehatters Computer Security Club. Using the format:
`http://fuzyll.com/csaw2015/<initials here>`
`http://fuzyll.com/csaw2015/wcsc` is the first part. It says:

```
CSAW 2015 FUZYLL RECON PART 2 OF ?: TmljZSB3b3JrISBUaGUgbmV4dCBwYXJ0IGlzIGF0IC9jc2F3MjAxNS88bXkgc3VwZXIgc21hc2ggYnJvdGhlcnMgbWFpbj4uCg==
```

The base64 translating to:

```
Nice work! The next part is at /csaw2015/<my super smash brothers main>.
```

Redbeard revealed it was yoshi, through a guess or knowing Alexander himself.

`http://fuzyll.com/csaw2015/yoshi` reveals nothing but an image of yoshi. Reverse image searches brought up nothing. But downloading the image and running `strings` on it gets:

```
CSAW 2015 FUZYLL RECON PART 3 OF ?: Isnt Yoshi the best?! The next egg in your hunt can be found at /csaw2015/<the cryptosystem I had to break in my first defcon qualifier>.
```

Going through a list of cryptosystems, `http://fuzyll.com/csaw2015/enigma` was the fourth part:

```javascript
CSAW 2015 FUZYLL RECON PART 4 OF 5: Okay, okay. This isnt Engima, but the next location was "encrypted" with the JavaScript below: Pla$ja|p$wpkt$kj$}kqv$uqawp$mw>$+gwes6451+pla}[waa[ia[vkhhmj

var s = "THIS IS THE INPUT"
var c = ""
for (i = 0; i < s.length; i++) {
    c += String.fromCharCode((s[i]).charCodeAt(0) ^ 0x4);
    }
    console.log(c);
```

When ORd with that same string, the encrypted string will show the plaintext. Plugging this into the Chrome Developer Console:

```javascript
var s = "Pla$ja|p$wpkt$kj$}kqv$uqawp$mw>$+gwes6451+pla}[waa[ia[vkhhmj"
var c = ""
for (i = 0; i < s.length; i++) {
    c += String.fromCharCode((s[i]).charCodeAt(0) ^ 0x4);
    }
```

The result is "The next stop on your quest is: /csaw2015/they_see_me_rollin".

FLAG:`flag{I_S3ARCH3D_HI6H_4ND_L0W_4ND_4LL_I_F0UND_W4S_TH1S_L0USY_FL4G}`
