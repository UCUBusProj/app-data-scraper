from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import time
import json
import sqlalchemy
from sqlalchemy import insert, MetaData, Table
from datetime import datetime, timezone
from os import environ

def connect():
    url = environ.get('DATABASE_URL')
    eng = sqlalchemy.create_engine(url, client_encoding='utf8', pool_size=1, pool_owerflow=0, pool_recycle=60, pool_timeout=60)
    meta = MetaData(eng)
    busdata = Table('busdata', meta, autoload=True, autoload_with=eng)
    connection = eng.connect()
    return connection, busdata

def insertData(data, connection, busdata):
    # Build an insert statement for the data table: stmt
	stmt = insert(busdata)
    # Execute stmt with the values_list: data
	results = connection.execute(stmt, data)
    # Return rowcount
	return results.rowcount

def hello():
	connection, busdata = connect()
	url = environ.get('ROUTE_URL')
	codes = ['LAD|712988','LAD|712991','LAD|713002','LAD|713010','LAD|1054553','LAD|949921','LAD|1723724','LAD|1527114']
	#code = 'LAD|712988'
	data = {}
	for code in codes:
		time.sleep(6)
		time1 = datetime.utcnow()
		time2 = datetime.utcnow()
		try:
			with urllib.request.urlopen(url+code) as response:
				time2 = datetime.utcnow()
				data[code] = json.loads(response.read().decode('utf-8').replace('"[', '[').replace(']"', ']').replace('\\"', '"'))
				for idx, dic in enumerate(data[code]):
					data[code][idx] = {k.lower(): v for k, v in dic.items()}
				rcnt = insertData(data[code], connection, busdata)
			time3 = datetime.utcnow()
			print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')+' Request time: '+str((time2-time1).seconds) + 's'+' DB time: '+str((time3-time2).seconds) + 's'+' row insert: ' + str(rcnt))
		except sqlalchemy.exc.OperationalError as e:
			print('Exc: ', e)
		except:
			print('Exc: Some else error')
	connection.close()

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
	hello()

sched.start()

