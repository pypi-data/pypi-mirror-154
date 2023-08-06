from . import settings

ENVS = {
  "local": "http://localhost:8000",
  "dev":   "https://api-dev.disent.com",
  "prod":  "https://snpricer-dev.disent.com",
  "demo": "https://snpricer-dev.disent.com",
}

def set_env(env):
	keys = ENVS.keys()
	if env in keys:
		before = settings.ENV
		if before != env:
			print(f"{before} is already selected")	
		settings.ENV = env
		print(f"{before} --> {settings.ENV}")
	else:
		raise Exception('Error',f'Environment must be one of {keys}')

def get_env():
	print(settings.ENV)


def get_uri_left():
	uri_left = ENVS[settings.ENV]
	return uri_left
