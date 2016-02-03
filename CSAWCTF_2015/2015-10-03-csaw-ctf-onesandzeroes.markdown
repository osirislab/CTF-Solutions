---
author: Hypersonic
comments: true
date: 2015-09-21 11:37+00:00
layout: post
slug: csaw-ctf-onesandzeroes
title: CSAW CTF 2015 - OnesAndZeroes
---

We notice that the file is just a bunch of ones and zeroes... let's try reading that as ascii bytes!

```
with open('onesandzeroes.mpeg') as f:
    contents = f.read()

def groups_of(s, n):
    return zip(*[iter(s)]*n)

''.join([chr(int(x, 2)) for x in map(''.join, groups_of(contents, 8))])
```

And we get our flag: `flag{People always make the best exploits.} I've never found it hard to hack most people. If you listen to them, watch them, their vulnerabilities are like a neon sign screwed into their heads.`
