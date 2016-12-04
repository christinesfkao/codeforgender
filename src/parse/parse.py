import subprocess
import sys
import os.path
from multiprocessing import Process
import datetime

def work(fn):
	try:
		if os.path.isfile("output_json/" + fn + ".json"):
			return
		subprocess.check_output("ruby sanitizing.rb", shell=True, input=("../Gossiping/" + fn).encode())
	except:
		print(fn, "error")
		subprocess.check_output("cp ../Gossiping/" + fn + " /var/www/html/Gossiping/", shell=True)

nth = 24

qs = []

for i in range(nth):
	qs.append([])

lns = 0

for fn in sys.stdin:
	qs[lns % nth].append(fn.strip())
	lns += 1

print("{0} jobs inserted".format(lns))

def doJob(que):
	print(str(len(que)) + " accepted", file=sys.stderr)
	for j in que:
		work(j)

thd = []

for i in range(24):
	thd.append(Process(target=doJob, args=(qs[i],)))
	thd[i].start()

print("start", file=sys.stderr)
print(datetime.datetime.now(), file=sys.stderr)

for i in range(24):
	thd[i].start()

for i in range(24):
	thd[i].join()

print("end", file=sys.stderr)
print(datetime.datetime.now(), file=sys.stderr)
