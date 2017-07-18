from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import time
import json
import sqlalchemy
from sqlalchemy import insert, MetaData, Table
	

def getEngine(user, password, db, host='ec2-107-22-162-158.compute-1.amazonaws.com', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    # The return value of create_engine() is our connection object
    eng = sqlalchemy.create_engine(url, client_encoding='utf8')
    return eng

def insertData(data):
	eng = getEngine('kdindhqkbfhvki', 'd95183fae29ec029684cdd9d25982535f1411d512974ff5ad14522118af26c47', 'dfg9jl6m1s681v')
	meta = MetaData(eng)
	busdata = Table('busdata', meta, autoload=True, autoload_with=eng)
	with eng.begin() as connection:
		# Build an insert statement for the data table: stmt
		stmt = insert(busdata)
		# Execute stmt with the values_list: results
		results = connection.execute(stmt, data)
		# Print rowcount
		print(results.rowcount)

def hello():
	codes = ['LAD|712988','LAD|712991','LAD|713002','LAD|713010','LAD|1054553','LAD|949921','LAD|1723724','LAD|1527114']
	#code = 'LAD|712988'
	data = {}
	for code in codes:
		time.sleep(5) 
		with urllib.request.urlopen('http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/RouteMonitoring/?code='+code) as response:
			data[code] = json.loads(response.read().decode('utf-8').replace('"[', '[').replace(']"', ']').replace('\\"', '"'))
			for idx, dic in enumerate(data[code]):
				data[code][idx] = {k.lower(): v for k, v in dic.items()}
				insertData(data[code])
			
	return str(data)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print(hello())

sched.start()

