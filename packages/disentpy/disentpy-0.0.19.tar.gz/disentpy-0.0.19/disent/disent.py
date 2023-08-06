
import io
import os
import sys
import urllib.parse as urllib_parse
import json

import time
import threading

import requests
import pandas as pd

APIKEY_FILENAME = 'apikey.json'

from . import settings
from . import env
from . import spinner

def disent_get(endpoint,uri_dict):
		apikey = verify_secrets()
		headers = {'Accept': 'application/json','Authorization': f'Api-Key {apikey}'}
		uri_params = urllib_parse.urlencode(uri_dict)
		uri_front = env.get_uri_left()
		url = f"{uri_front}/{endpoint}?{uri_params}"
		
		response = None
		try:
			t = threading.Thread(target=spinner.bouncing_ball, args=(endpoint,))
			t.start()
			response = requests.request("GET", url, headers=headers)
			t.do_run = False		
		except (KeyboardInterrupt,SystemExit,Exception):
			t.do_run = False	
			raise
		
		if response is None:
			print('Reponse not found.')

		total_size_in_bytes= int(response.headers.get('content-length', 0))/1024
		print('Downloaded........',f"{round(total_size_in_bytes,0)} KiB done.                ")

		txt = response.text
		
		d = json.loads(txt)
		result = d.get('result',None)
		if result is None:
			raise Exception('Server error',d['Exception'])
			
		df = pd.DataFrame(result)
		return df

def verify_secrets():
	dir = os.path.join(os.path.expanduser('~'),'.disent')
	if not os.path.isdir(dir):
		os.makedirs(dir, exist_ok=True)
	filename = os.path.join(dir,APIKEY_FILENAME)

	try:
		with open(filename) as f:
			try:
				d = json.load(f)
				apikey = d.get('Api-Key',None)
				if apikey is None:
					raise Exception('Error','Secrets file is missing Api-Key.')
			except:
				raise Exception('Error','Secrets file is invalid.')
				
	except FileNotFoundError:
		print('Secrets file not found. See docs.')
		apikey = input("Enter your API-Key to continue: ")
		d = {'Api-Key':apikey}
		with open(filename,'w') as f:
			json.dump(d,f)
	
	return apikey

def example():
	d = {'source':'BSPLINE_MODEL','ticker':'AAPL'}
	result = disent('cache',d)
	return result

def disent(model,kwargs):
	models = {
		'cache':'api/cache'
	}
	model_endpoint = models[model]
	result =  disent_get(model_endpoint,kwargs)
	return result

def hub(model,kwargs,):
	kwargs['source']=model
	model_endpoint='api/cache'
	result =  disent_get(model_endpoint,kwargs)
	return result



def unit_test():
	d = {
		# "source":"BSPLINE_MODEL",
		"source":"VOLS_ORATS",
		"datastorekey":":::snapshots:20220606:211511:market_data_snapshot",
		"ticker":"SPX",
		# "pivot":"YRS,MNY,IV"
	}
	df = disent('cache',d)
	print(df)


if __name__=='__main__':
	unit_test()
