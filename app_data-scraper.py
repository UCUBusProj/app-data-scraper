from flask import Flask

import urllib.request
import time
import json

app_finl = Flask(__name__)

@app_finl.route('/')
def hello():
	codes = ['LAD|712988','LAD|712991','LAD|713002','LAD|713010','LAD|1054553','LAD|949921','LAD|1723724','LAD|1527114']
	code = 'LAD|712988'
	data = {}
	#for code in codes:
		#time.sleep(5) 
	with urllib.request.urlopen('http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/RouteMonitoring/?code='+code) as response:
		data[code] = response.read()
	parsed_json = json.loads(data[codes[0]].decode('utf-8').replace('"[', '[').replace(']"', ']').replace('\\"', '"'))
	return str(parsed_json[7])

if __name__ == '__main__':
    app_finl.run()