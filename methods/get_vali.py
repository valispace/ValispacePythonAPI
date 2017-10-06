from lib import *
from helpers import name_to_id

def get_vali(id=None, name=None):
# ValispaceGetVali returns the correct Vali. Input can be id or name

	# Checks Authentication
	if not hasattr(globals, 'valispace_login'):
		print 'VALISPACE-ERROR: You first have to run valispace.init()'
		return
	
	# Checks if argument was passed
	if id is None and name is None:
		print "VALISPACE-ERROR: 1 argument expected (name or id)"
		return

	if id is None:
		# Name argument was passed
		id = name_to_id(name)
	
	url = globals.valispace_login['url'] + "vali/" + str(id) + "/"
	headers = globals.valispace_login['options']['Headers']
	
	return requests.get(url, headers=headers).json()