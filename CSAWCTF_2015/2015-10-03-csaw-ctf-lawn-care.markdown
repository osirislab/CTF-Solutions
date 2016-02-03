---
author: ghost
comments: true
date: 2015-10-03 11:37+00:00
layout: post
slug: csaw-ctf-lawn-care
title: CSAW CTF 2015 - Lawn Care Simulator
---

After browsing around the home page of the website given, we notice 2 suspect things: password MD5s are computed client side, and there is a version number at the bottom of the page. After inspecting in chrome dev tools, we see that the version number is dynamically pulled from `/.git/refs/heads/master`, meaning that the site's .git is publically accessible. However, while we can read files, directory listings are turned off. After researching the basics of how git works, we grab `/.git/index` which contains the filenames and sha1 hashes of all files in the repo. Running this through a git index parser (e.g. [gin](https://github.com/sbp/gin)), we get a list of all the files and hashes:

```
[entry]
  entry = 6
  ctime = 1442601441.844829
  mtime = 1442601077.0
  dev = 41
  ino = 118
  mode = 100644
  uid = 0
  gid = 0
  size = 918
  sha1 = 73009145aac48cf1d0e72adfaa093de11f491715
  flags = 11
  assume-valid = False
  extended = False
  stage = (False, False)
  name = premium.php

[entry]
  entry = 7
  ctime = 1442601441.844829
  mtime = 1442601077.0
  dev = 41
  ino = 117
  mode = 100644
  uid = 0
  gid = 0
  size = 2937
  sha1 = 8e4852023815dc70761e38cde28aebed9ec038e3
  flags = 11
  assume-valid = False
  extended = False
  stage = (False, False)
  name = sign_up.php

[entry]
  entry = 8
  ctime = 1442601441.844829
  mtime = 1442601077.0
  dev = 41
  ino = 121
  mode = 100644
  uid = 0
  gid = 0
  size = 780
  sha1 = 637c8e963a5fb7080ff639b5297bb10bca491bda
  flags = 17
  assume-valid = False
  extended = False
  stage = (False, False)
  name = validate_pass.php

[checksum]
  checksum = True
  sha1 = b8b3adcc3ab5fcfb1639c9041dcdf2864d098202
```

All files in git are stored in `.git/objects/{first 2 chars of file sha1}/{rest of file sha1}`. Since we have the sha1 hashes from the git index file, we are able to download all of the files in the repo.

After zlib decoding all of the files, we have the entire source of the site’s backend (with the exception of db.php) – premium.php, sign\_up.php, and validate\_pass.php. After browsing through these, we find that sign\_up.php can leak the username we need if we just request the username ‘%’. We did so, and found the username to be ‘\~\~FLAG\~\~’. We also noted that the password validation function `validate` in validate\_pass.php has a trivial timing exploit that allows us to leak the md5 of the password - `usleep(300000)` is called whenever a correct character is sent:

```php
function validate($user, $pass) {
    ...
    if (strlen($pass) != strlen($hash))
        return False;

    $index = 0;
    while($hash[$index]){
        if ($pass[$index] != $hash[$index])
            return false;
        # Protect against brute force attacks
        usleep(300000);
        $index+=1;
    }

    return true;
}
?>
```

This means that the more characters correct we get, the longer the delay is. In addition, as noted above, the client hashes the password, so we do not need to worry about cracking the password, we just need to recover it.

After writing a python script to exploit the timing vulnerability, we arrived at the 10th character in the hash. No matter which ASCII character was sent for this place in the hash, the delay received from the server would not change. After some time, it was discovered that the loop that validates the MD5s is incorrectly implemented. The trouble statement is ` while($hash[$index]) {…`. While at first glance this appears to be valid (all ASCII chars are > 0), PHP type casts these characters into ints, and the 10th character happens to be a 0. Because of this, the server drops out of the loop, and any md5 with the correct first 10 characters is a valid login hash. Finally, we send the username and the hash to premium.php which returns our flag.
