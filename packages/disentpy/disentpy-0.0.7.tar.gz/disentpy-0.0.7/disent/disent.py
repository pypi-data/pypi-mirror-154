import requests
import pandas as pd
import json
import os
import urllib.parse as urllib_parse
import io
import time
import threading

APIKEY_FILENAME = '~/.disent/apikey.json'
DEFAULT_ENV = 'prod'
ENVS_FILENAME = 'envs.json'


def spinner(arg):
	x = [
			"( ●    )",
			"(  ●   )",
			"(   ●  )",
			"(    ● )",
			"(     ●)",
			"(    ● )",
			"(   ●  )",
			"(  ●   )",
			"( ●    )",
			"(●     )"
	]
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		print(f'Executing {arg}........',x[0],end='\r')
		x=x[1:]+[x[0]]
		time.sleep(0.05)

def disent_get(protocol,hostname_port,endpoint,uri_dict):
		apikey = verify_secrets()
		headers = {'Accept': 'application/json','Authorization': f'Api-Key {apikey}'}
		uri_params = urllib_parse.urlencode(uri_dict)
		url = f"{protocol}://{hostname_port}/{endpoint}?{uri_params}"
		t = threading.Thread(target=spinner, args=(endpoint,))
		t.start()
		response = requests.request("GET", url, headers=headers)
		t.do_run = False
		
		total_size_in_bytes= int(response.headers.get('content-length', 0))/1024

		print('Downloaded........',f"{round(total_size_in_bytes,0)}KiB done.")
		
		txt = response.text
		
		d = json.loads(txt)
		result = d.get('result',None)
		if result is None:
			raise Exception('Server error',d['Exception'])
			
		df = pd.DataFrame(result)
		return df

def verify_secrets():
	try:
		apikey_filename_expanded = os.path.expanduser(APIKEY_FILENAME)
		with open(apikey_filename_expanded) as f:
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
		apikey_filename_expanded = os.path.expanduser(APIKEY_FILENAME)
		with open(apikey_filename_expanded,'w') as f:
			json.dump(d,f)
	
	return apikey

def example(env='prod'):
	d = {'source':'BSPLINE_MODEL','ticker':'AAPL'}
	result = disent('cache',d,env=env)
	return result

def get_env_tuple(env):
	path = os.path.dirname(__file__)
	filename = os.path.join(path, ENVS_FILENAME)
	f = open(filename)
	d = json.load(f)
	result = d[env]
	return result

def disent(model,kwargs,env='prod'):
	protocol, hostname_port = get_env_tuple(env)
	models = {
		'cache':'api/cache'
	}
	model_endpoint = models[model]
	result =  disent_get(protocol,hostname_port,model_endpoint,kwargs)
	return result

def hub(model,kwargs,env='prod'):
	protocol, hostname_port = get_env_tuple(env)
	kwargs['source']=model
	model_endpoint='api/cache'
	result =  disent_get(protocol,hostname_port,model_endpoint,kwargs)
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
