
import io
import os
import re
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
		verified = False
		isDeleted = False
		while not verified:
			apikey = verify_secrets(isDeleted=isDeleted)
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
			if 'Error' in d:
				if 'Authentication' in d['Error']:
					verify_secrets(removeKey=True)
					isDeleted=True
				else:
					raise Exception('Error','Unhandled server error. Please try again.')
			elif 'result' in d:
				verified = True

		result = d.get('result',None)
		if result is None:
			raise Exception('Server error',d['Exception'])

		try:	
			df = pd.DataFrame(result)
			if settings.DF_DATE_FORMAT == 'datetime':
				for c in df.columns:
					if c.upper() in ['DT','DATE']:
						df[c] = pd.to_datetime(df[c])
			retValue = df
		except:
			retValue = result
		
		return retValue

def fetch_temp_key(email):
	reponse = requests.get(f'{env.get_uri_left}/api/keygen?email={email}')
	d = json.loads(reponse.text)
	if 'Result' in d:
		key = d['Result']
		return key
	else:
		raise Exception('Error','Error in generating temp key. Contact support@disent.com.')


def verify_secrets(removeKey=False,isDeleted=False):
	dir = os.path.join(os.path.expanduser('~'),'.disent')
	if not os.path.isdir(dir):
		os.makedirs(dir, exist_ok=True)
	filename = os.path.join(dir,APIKEY_FILENAME)

	if removeKey:
		os.remove(filename)
		return 

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
		if isDeleted:
			print('\nSupplied key is not valid. See docs.')
		else:
			print('\nKey not found. See docs.')
		print('')
		choice = input('Do you have a permanent key (1) or would like you to request a temporary key (2): ')
		if choice == '1':
			apikey = input("Enter your key to continue: ")
		if choice == '2':
			notValid = True
			while notValid:
				email = input("Please provide a valid email address: ")
				regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
				if re.fullmatch(regex, email):
					apikey = fetch_temp_key(email)
					notValid = False
				else:
					print('Invalid email. Try again.')
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
