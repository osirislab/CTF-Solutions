import subprocess
import signal

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

ranges = range(0x400000, 0x401000)

for b in ranges:
	for bit in range(b*8, (b+1)*8):
		print bit
		proc = subprocess.Popen(['./butterfly'], stdin=subprocess.PIPE, stdout=open('/dev/null'))
		signal.signal(signal.SIGALRM, alarm_handler)
		signal.alarm(1)
		try:
			proc.communicate(str(bit) + '\n')
			signal.alarm(0)
		except Alarm:
			print "SOMETHING INTERESTING HAPPENED AT", bit
		
		if proc.poll() is None:
			proc.kill()
