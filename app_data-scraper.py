from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import time
import json
	
def hello():
	codes = ['LAD|712988','LAD|712991','LAD|713002','LAD|713010','LAD|1054553','LAD|949921','LAD|1723724','LAD|1527114']
	#code = 'LAD|712988'
	data = {}
	for code in codes:
		time.sleep(5) 
		with urllib.request.urlopen('http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/RouteMonitoring/?code='+code) as response:
			data[code] = json.loads(response.read().decode('utf-8').replace('"[', '[').replace(']"', ']').replace('\\"', '"'))
	return str(data)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    print(hello())

sched.start()

