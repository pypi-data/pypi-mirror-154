from . import settings

def set(env):
	keys = settings.ENVS.keys()
	if env in keys:
		before = settings.ENV
		if before != env:
			print(f"{before} is already selected")	
		settings.ENV = env
		print(f"{before} --> {settings.ENV}")
	else:
		raise Exception('Error',f'Environment must be one of {keys}')

def get():
	print(settings.ENV)


def get_uri_left():
	uri_left = settings.ENVS[settings.ENV]
	return uri_left
