---
author: ghost
comments: true
date: 2015-10-03 11:37+00:00
layout: post
slug: csaw-ctf-sharpturn
title: CSAW CTF 2015 - Sharpturn
---

We’re given a .tar.xz which contains a partially corrupted git repo. Running `git log` reveals 4 commits, which all primarily build out one main .c file:

```
commit 4a2f335e042db12cc32a684827c5c8f7c97fe60b
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:11:05 2015 -0700

    All done now! Should calculate the flag..assuming everything went okay.

commit d57aaf773b1a8c8e79b6e515d3f92fc5cb332860
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:09:31 2015 -0700

    There's only two factors. Don't let your calculator lie.

commit 2e5d553f41522fc9036bacce1398c87c2483c2d5
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:08:51 2015 -0700

    It's getting better!

commit 7c9ba8a38ffe5ce6912c69e7171befc64da12d4c
Author: sharpturn <csaw@isis.poly.edu>
Date:   Sat Sep 5 18:08:05 2015 -0700

    Initial commit! This one should be fun.
```

However if we run `git fsck` (as later put in as the problem’s hint), we notice that there are 3 corrupt blobs, corresponding to the 3 non-initial commits:

```
Checking object directories: 100% (256/256), done.
error: sha1 mismatch 354ebf392533dce06174f9c8c093036c138935f3
error: 354ebf392533dce06174f9c8c093036c138935f3: object corrupt or missing
error: sha1 mismatch d961f81a588fcfd5e57bbea7e17ddae8a5e61333
error: d961f81a588fcfd5e57bbea7e17ddae8a5e61333: object corrupt or missing
error: sha1 mismatch f8d0839dd728cb9a723e32058dcc386070d5e3b5
error: f8d0839dd728cb9a723e32058dcc386070d5e3b5: object corrupt or missing
missing blob 354ebf392533dce06174f9c8c093036c138935f3
missing blob f8d0839dd728cb9a723e32058dcc386070d5e3b5
missing blob d961f81a588fcfd5e57bbea7e17ddae8a5e61333
```

After zlib-decoding the first corrupted blob (354ebf3…), the string "51337" stands out as strange (the '5' in particular). Assuming this challenge is feasible, we assume that there is only one or two characters in the blob that have been changed. After writing a quick python script which automatically tries substituting each ASCII printable character in a particular space, we run the script against this blob, assuming the character '5' in '51337' has been modified. The script successfully changes the 5 into a 3, and the hash is now valid.

This script was then run again on the second blob (d961f81...) after manually changing the 51337 into 31337, and the script successfully found a hash match by changing '270031727027' into '272031727027'. After applying both of these changes to the final blob with an incorrect hash (f8d0839...), we noticed that the flag was not properly cout’d (the line was `cout << &lag`). We assumed that the character flip in this blob was changing ‘f’ to ‘&’ in `cout << flag`, and were correct. After extracting the code from the final blob, making the 3 changes, and compiling, getting the flag is as simple as following the directions of the program.

The final script is below:

```python
import sys, string, os

orig = open(sys.argv[1]).read().decode('zlib')
print orig

pos = input("Indexes? ")

for p in pos:
    for c in string.digits:
        o = orig[:p]+c+orig[p+1:]
        f = open(sys.argv[1],'w')
        f.write(o.encode('zlib'))
        f.close()
        if sys.argv[1] not in os.popen("git fsck").read():
            print "Found"
            os._exit(0)

print "No matches"
f = open(sys.argv[1],'w')
f.write(orig.encode('zlib'))
f.close()
```
